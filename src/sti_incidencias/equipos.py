from __future__ import annotations
from mysql.connector.connection import MySQLConnection
from .db import fetch_all, execute

def listar_equipos(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve todos los equipos ordenados por nombre.
    """
    sql = "SELECT * FROM equipos ORDER BY nombre ASC"
    return fetch_all(conn, sql)

def buscar_equipo_por_id(conn: MySQLConnection, equipo_id: int) -> dict | None:
    """
    Busca un equipo por su ID.
    Devuelve None si no existe.
    """
    sql = "SELECT * FROM equipos WHERE id = %s"
    resultados = fetch_all(conn, sql, (equipo_id,))
    return resultados[0] if resultados else None

def crear_equipo(conn: MySQLConnection, nombre: str, tipo: str = None) -> int:
    """
    Crea un nuevo equipo.
    Devuelve el número de filas afectadas.
    """
    if not nombre or nombre.isspace():
        raise ValueError("El nombre no puede estar vacío")
    
    sql = "INSERT INTO equipos (nombre, tipo) VALUES (%s, %s)"
    return execute(conn, sql, (nombre, tipo))