from persistencia.conexion import (abrir_conexion, obtener_motor)


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    if obtener_motor() == "sqlite":
        sql_empleado = '''
        CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL,
        departamento TEXT
        )
        '''

        sql_departamento = '''
        CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
        )
        '''
    else:
        sql_empleado = '''
        CREATE TABLE IF NOT EXISTS empleado (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(150) NOT NULL,
        departamento VARCHAR(100)
        )
        '''
        
        sql_departamento = '''
        CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100)
        )
        '''
    cursor.execute(sql_empleado)
    cursor.execute(sql_departamento)
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")
