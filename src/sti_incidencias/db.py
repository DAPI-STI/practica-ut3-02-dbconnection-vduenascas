from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable, Optional

import mysql.connector
from mysql.connector.connection import MySQLConnection


@dataclass(frozen=True)
class DBConfig:
    """Configuración de conexión a la base de datos."""
    host: str
    port: int
    database: str
    user: str
    password: str


def load_config_from_env() -> DBConfig:
    """
    Lee la configuración de conexión desde variables de entorno.

    Variables esperadas (con valores por defecto):
    - DB_HOST (default: localhost)
    - DB_PORT (default: 3306)
    - DB_NAME (default: sti_incidencias)
    - DB_USER (default: sti_app)
    - DB_PASSWORD (default: sti_app_2026)

    Debe devolver un objeto DBConfig correctamente construido.

    Recomendación:
    - Validar que DB_PORT sea un número entero.
    """
    host = os.environ.get('DB_HOST', 'localhost')
    
    port_str = os.environ.get('DB_PORT', '3306')
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"DB_PORT debe ser un número entero, se obtuvo: {port_str}")
    
    database = os.environ.get('DB_NAME', 'sti_incidencias')
    user = os.environ.get('DB_USER', 'sti_app')
    password = os.environ.get('DB_PASSWORD', 'sti_app_2026')
    
    return DBConfig(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )


def get_connection(cfg: Optional[DBConfig] = None) -> MySQLConnection:
    """
    Crea y devuelve una conexión MySQL/MariaDB.

    - Si cfg es None, debe llamar a load_config_from_env().
    - Debe usar mysql.connector.connect(...) con los parámetros de cfg.
    """
    if cfg is None:
        cfg = load_config_from_env()
    
    try:
        conn = mysql.connector.connect(
            host=cfg.host,
            port=cfg.port,
            database=cfg.database,
            user=cfg.user,
            password=cfg.password
        )
        return conn
    except mysql.connector.Error as e:
        raise ConnectionError(f"No se pudo conectar a MySQL: {e}")


def fetch_all(conn: MySQLConnection, query: str, params: Optional[Iterable[Any]] = None) -> list[dict]:
    """
    Ejecuta una consulta SELECT y devuelve una lista de diccionarios (una fila -> un dict).

    Pistas:
    - Crear un cursor con conn.cursor(dictionary=True)
    - Ejecutar cur.execute(query, params o ())
    - Obtener filas con cur.fetchall()
    - Cerrar el cursor siempre (try/finally)
    """
    cursor = conn.cursor(dictionary=True)
    try:
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        resultados = cursor.fetchall()
        return resultados
    finally:
        cursor.close()


def execute(conn: MySQLConnection, query: str, params: Optional[Iterable[Any]] = None) -> int:
    """
    Ejecuta una sentencia INSERT/UPDATE/DELETE y devuelve el número de filas afectadas.

    Pistas:
    - Crear un cursor normal conn.cursor()
    - Ejecutar cur.execute(query, params o ())
    - Hacer conn.commit()
    - Devolver cur.rowcount
    - Cerrar el cursor siempre (try/finally)
    """
    cursor = conn.cursor()
    try:
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        filas_afectadas = cursor.rowcount
        return filas_afectadas
    finally:
        cursor.close()