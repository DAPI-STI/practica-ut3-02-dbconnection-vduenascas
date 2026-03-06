from __future__ import annotations
from mysql.connector.connection import MySQLConnection
from .db import execute, fetch_all

def listar_incidencias_activas(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve incidencias cuyo estado NO sea 'cerrada'.
    Ordena por prioridad (alta > media > baja) y luego por fecha_apertura ascendente.
    """
    sql = """
        SELECT * FROM incidencias
        WHERE estado != 'cerrada'
        ORDER BY 
            CASE prioridad
                WHEN 'alta' THEN 1
                WHEN 'media' THEN 2
                WHEN 'baja' THEN 3
                ELSE 4
            END,
            fecha_apertura ASC
    """
    return fetch_all(conn, sql)


def listar_incidencias_sin_tecnico(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve incidencias activas sin técnico asignado.
    """
    sql = """
        SELECT * FROM incidencias
        WHERE tecnico_id IS NULL AND estado != 'cerrada'
        ORDER BY fecha_apertura ASC
    """
    return fetch_all(conn, sql)


def crear_incidencia(conn: MySQLConnection, equipo_id: int, descripcion: str, prioridad: str = "media") -> int:
    """
    Crea una incidencia nueva en estado 'abierta'.
    """
    # Validaciones
    if not descripcion or descripcion.isspace():
        raise ValueError("La descripción no puede estar vacía")
    
    if prioridad not in ['baja', 'media', 'alta']:
        raise ValueError("Prioridad debe ser 'baja', 'media' o 'alta'")
    
    if not isinstance(equipo_id, int) or equipo_id <= 0:
        raise ValueError("equipo_id debe ser un entero positivo")
    
    # Inserción
    sql = """
        INSERT INTO incidencias 
        (equipo_id, descripcion, prioridad, estado, fecha_apertura, tecnico_id, fecha_cierre)
        VALUES (%s, %s, %s, 'abierta', NOW(), NULL, NULL)
    """
    cursor = conn.cursor()
    cursor.execute(sql, (equipo_id, descripcion, prioridad))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    return filas


def asignar_tecnico(conn: MySQLConnection, incidencia_id: int, tecnico_id: int) -> int:
    """
    Asigna un técnico a una incidencia y la marca como 'en_proceso'.
    """
    # Validaciones
    if not isinstance(incidencia_id, int) or incidencia_id <= 0:
        raise ValueError("incidencia_id debe ser un entero positivo")
    
    if not isinstance(tecnico_id, int) or tecnico_id <= 0:
        raise ValueError("tecnico_id debe ser un entero positivo")
    
    # Actualización
    sql = """
        UPDATE incidencias
        SET tecnico_id = %s, estado = 'en_proceso'
        WHERE id = %s AND estado != 'cerrada'
    """
    cursor = conn.cursor()
    cursor.execute(sql, (tecnico_id, incidencia_id))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    return filas


def cerrar_incidencia(conn: MySQLConnection, incidencia_id: int) -> int:
    """
    Cierra una incidencia.
    """
    # Validación
    if not isinstance(incidencia_id, int) or incidencia_id <= 0:
        raise ValueError("incidencia_id debe ser un entero positivo")
    
    # Actualización
    sql = """
        UPDATE incidencias
        SET estado = 'cerrada', fecha_cierre = NOW()
        WHERE id = %s AND estado != 'cerrada'
    """
    cursor = conn.cursor()
    cursor.execute(sql, (incidencia_id,))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    return filas


def detalle_incidencias_join(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve una vista enriquecida con datos de equipo y técnico.
    """
    sql = """
        SELECT 
            i.id, i.descripcion, i.prioridad, i.estado, 
            i.fecha_apertura, i.fecha_cierre,
            e.tipo, e.modelo, e.ubicacion, e.estado AS estado_equipo,
            t.nombre AS tecnico
        FROM incidencias i
        JOIN equipos e ON i.equipo_id = e.id
        LEFT JOIN tecnicos t ON i.tecnico_id = t.id
        ORDER BY 
            CASE i.estado
                WHEN 'abierta' THEN 1
                WHEN 'en_proceso' THEN 2
                WHEN 'cerrada' THEN 3
                ELSE 4
            END,
            CASE i.prioridad
                WHEN 'alta' THEN 3
                WHEN 'media' THEN 2
                WHEN 'baja' THEN 1
            END DESC,
            i.fecha_apertura ASC
    """
    return fetch_all(conn, sql)