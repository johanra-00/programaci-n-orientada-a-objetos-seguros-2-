
from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
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
            horas_registradas REAL NOT NULL
        )
        """

        sql_usuario = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            empleado_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        )
        """

    else:
        sql_empleado = """
        CREATE TABLE IF NOT EXISTS empleado (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(150) NOT NULL,
            departamento VARCHAR(100)
        )
        """

        sql_departamento = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL
        )
        """

        sql_proyecto = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT
        )
        """

        sql_registro_tiempo = """
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fecha_registro DATE NOT NULL,
            horas_registradas DECIMAL(5,2) NOT NULL
        )
        """

        sql_usuario = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            empleado_id INT NOT NULL UNIQUE,
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
