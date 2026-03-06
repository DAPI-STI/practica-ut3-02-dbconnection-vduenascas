from __future__ import annotations
from mysql.connector.connection import MySQLConnection
from .db import fetch_all, execute

def listar_tecnicos(conn: MySQLConnection) -> list[dict]:
    """
    Devuelve todos los técnicos ordenados por nombre.
    """
    sql = "SELECT * FROM tecnicos ORDER BY nombre ASC"
    return fetch_all(conn, sql)

def buscar_tecnico_por_id(conn: MySQLConnection, tecnico_id: int) -> dict | None:
    """
    Busca un técnico por su ID.
    Devuelve None si no existe.
    """
    sql = "SELECT * FROM tecnicos WHERE id = %s"
    resultados = fetch_all(conn, sql, (tecnico_id,))
    return resultados[0] if resultados else None

def crear_tecnico(conn: MySQLConnection, nombre: str, email: str) -> int:
    """
    Crea un nuevo técnico.
    Devuelve el número de filas afectadas.
    """
    if not nombre or nombre.isspace():
        raise ValueError("El nombre no puede estar vacío")
    if not email or email.isspace():
        raise ValueError("El email no puede estar vacío")
    
    sql = "INSERT INTO tecnicos (nombre, email) VALUES (%s, %s)"
    return execute(conn, sql, (nombre, email))