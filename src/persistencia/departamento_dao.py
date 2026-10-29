
from persistencia.conexion import abrir_conexion, obtener_motor


class DepartamentoDAO:

    @staticmethod
    def insertar(departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            cursor.execute(
                f"INSERT INTO departamento (nombre) VALUES ({marcador})",
                (departamento.nombre,)
            )
            departamento.id_departamento = cursor.lastrowid
            conexion.commit()
            return departamento
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM departamento")
            return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def buscar(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"SELECT id, nombre FROM departamento WHERE id = {marcador}",
                (id_departamento,)
            )
            return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_departamento, nombre):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"UPDATE departamento SET nombre = {marcador} "
                f"WHERE id = {marcador}",
                (nombre, id_departamento)
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"DELETE FROM departamento WHERE id = {marcador}",
                (id_departamento,)
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()
