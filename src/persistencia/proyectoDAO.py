
from dominio.proyecto import Proyecto
from persistencia.conexion import abrir_conexion, obtener_motor


class ProyectoDAO:

    @staticmethod
    def _convertir(fila):
        proyecto = Proyecto(
            nombre=fila[1],
            descripcion=fila[2],
            cantidad_empleados=0
        )
        proyecto.id = fila[0]
        return proyecto

    @staticmethod
    def insertar(proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""
                INSERT INTO proyecto (nombre, descripcion)
                VALUES ({marcador}, {marcador})
            """
            cursor.execute(sql, (proyecto.nombre, proyecto.descripcion))
            proyecto.id = cursor.lastrowid
            conexion.commit()
            return proyecto
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre, descripcion FROM proyecto"
            )
            return [
                ProyectoDAO._convertir(fila)
                for fila in cursor.fetchall()
            ]
        finally:
            conexion.close()

    @staticmethod
    def buscar(id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            cursor.execute(
                f"SELECT id, nombre, descripcion FROM proyecto "
                f"WHERE id = {marcador}",
                (id_proyecto,)
            )
            fila = cursor.fetchone()

            if fila is None:
                return None

            return ProyectoDAO._convertir(fila)
        finally:
            conexion.close()

    @staticmethod
    def actualizar(proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""
                UPDATE proyecto
                SET nombre = {marcador},
                    descripcion = {marcador}
                WHERE id = {marcador}
            """
            cursor.execute(
                sql,
                (proyecto.nombre, proyecto.descripcion, proyecto.id)
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            cursor.execute(
                f"DELETE FROM proyecto WHERE id = {marcador}",
                (id_proyecto,)
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()
