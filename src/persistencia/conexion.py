import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()


def obtener_motor():
    return os.getenv("DB_ENGINE", "mysql").lower()


def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        return sqlite3.connect(
            os.getenv("DB_NAME", "ecotech.db")
        )

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )

    raise ValueError(f"Motor no soportado: {motor}")


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    sql_empleado = """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL,
        departamento TEXT
    )
    """

    sql_departamento = """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """

    sql_proyecto = """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    )
    """

    sql_registro_tiempo = """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_registro TEXT NOT NULL,
        horas_registradas REAL NOT NULL,
        empleado_id INTEGER NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id)
    )
    """

    sql_usuario = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'empleado'CHECK (rol IN ('admin', 'empleado')),
        empleado_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id)
    )
    """

    cursor.execute(sql_empleado)
    cursor.execute(sql_departamento)
    cursor.execute(sql_proyecto)
    cursor.execute(sql_registro_tiempo)
    cursor.execute(sql_usuario)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")