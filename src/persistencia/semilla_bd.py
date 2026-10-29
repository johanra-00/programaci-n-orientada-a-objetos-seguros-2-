from persistencia.conexion import abrir_conexion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.UsuarioDAO import UsuarioDAO
from servicios.autenticacion import registrar_usuario
from getpass import getpass

def cargar_departamentos(conexion):
    cursor = conexion.cursor()

    departamentos = [
        "Tecnologia",
        "Recursos Humanos",
        "Marketing",
        "Finanzas",
        "Operaciones"
    ]

    for nombre in departamentos:
        cursor.execute(
            "SELECT id FROM departamento WHERE nombre = ?",
            (nombre,)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO departamento (nombre) VALUES (?)",
                (nombre,)
            )
            print("Departamento creado:", nombre)
        else:
            print("Departamento ya existe:", nombre)


def cargar_empleados(conexion):
    cursor = conexion.cursor()

    empleados = [
        ("Ana Torres", "ana.torres@ecotech.example", "Tecnologia"),
        ("Luis Perez", "luis.perez@ecotech.example", "Tecnologia"),
        ("Maria Soto", "maria.soto@ecotech.example", "Tecnologia"),
        ("Pedro Rojas", "pedro.rojas@ecotech.example", "Tecnologia"),
        ("Camila Diaz", "camila.diaz@ecotech.example", "Recursos Humanos"),
        ("Diego Silva", "diego.silva@ecotech.example", "Recursos Humanos"),
        ("Sofia Castro", "sofia.castro@ecotech.example", "Recursos Humanos"),
        ("Matias Lopez", "matias.lopez@ecotech.example", "Recursos Humanos"),
        ("Valentina Ruiz", "valentina.ruiz@ecotech.example", "Marketing"),
        ("Javier Flores", "javier.flores@ecotech.example", "Marketing"),
        ("Daniela Reyes", "daniela.reyes@ecotech.example", "Marketing"),
        ("Nicolas Vega", "nicolas.vega@ecotech.example", "Marketing"),
        ("Fernanda Molina", "fernanda.molina@ecotech.example", "Finanzas"),
        ("Andres Herrera", "andres.herrera@ecotech.example", "Finanzas"),
        ("Paula Navarro", "paula.navarro@ecotech.example", "Finanzas"),
        ("Cristobal Torres", "cristobal.torres@ecotech.example", "Finanzas"),
        ("Gabriela Morales", "gabriela.morales@ecotech.example", "Operaciones"),
        ("Felipe Contreras", "felipe.contreras@ecotech.example", "Operaciones"),
        ("Antonia Vargas", "antonia.vargas@ecotech.example", "Operaciones"),
        ("Sebastian Fuentes", "sebastian.fuentes@ecotech.example", "Operaciones")
    ]

    for nombre, correo, departamento in empleados:
        cursor.execute(
            "SELECT id FROM empleado WHERE correo = ?",
            (correo,)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                """
                INSERT INTO empleado (nombre, correo, departamento)
                VALUES (?, ?, ?)
                """,
                (nombre, correo, departamento)
            )
            print("Empleado creado:", nombre)
        else:
            print("Empleado ya existe:", correo)


def cargar_semilla():
    conexion = abrir_conexion()

    try:
        cargar_departamentos(conexion)
        cargar_empleados(conexion)
        conexion.commit()
        print("Semilla cargada correctamente.")

    except Exception as error:
        conexion.rollback()
        print("Error al cargar la semilla:", error)
        raise

    finally:
        conexion.close()

def cargar_admin():
    empleado = EmpleadoDAO.buscar_por_correo(
        "ana.torres@ecotech.example"
    )

    if empleado is None:
        print("No se encontró el empleado para admin.")
        return

    cuenta = UsuarioDAO.buscar_por_empleado(empleado.id)

    if cuenta is not None:
        print("La cuenta admin ya existe.")
        return

    clave = getpass("Crea la contraseña para admin: ")

    registrar_usuario(
        empleado.id,
        "admin",
        clave
    )

    print("Cuenta admin creada correctamente.")


if __name__ == "__main__":
    cargar_semilla()
    cargar_admin()