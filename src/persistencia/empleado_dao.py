from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoDAO:

    @staticmethod
    def _convertir_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2],
            departamento=fila[3],
            telefono="",
            sueldo=0
        )

    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
        INSERT INTO empleado (nombre, correo, departamento)
        VALUES ({marcador}, {marcador}, {marcador})
        """

        cursor.execute(
            sql,
            (
                empleado.nombre,
                empleado.correo,
                empleado.departamento
            )
        )

        empleado.id = cursor.lastrowid

        conexion.commit()
        conexion.close()

        return empleado

    @staticmethod
    def obtener_por_id(id):
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
        SELECT id, nombre, correo, departamento
        FROM empleado
        WHERE id = {marcador}
        """

        cursor.execute(sql, (id,))
        fila = cursor.fetchone()

        conexion.close()

        if fila is None:
            return None

        return EmpleadoDAO._convertir_a_empleado(fila)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sql = """
        SELECT id, nombre, correo, departamento
        FROM empleado
        """

        cursor.execute(sql)
        filas = cursor.fetchall()

        conexion.close()

        empleados = []

        for fila in filas:
            empleados.append(
                EmpleadoDAO._convertir_a_empleado(fila)
            )

        return empleados

    @staticmethod
    def actualizar(empleado):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()

            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""
            UPDATE empleado
            SET nombre = {marcador}, correo = {marcador}
            WHERE id = {marcador}
            """

            cursor.execute(
                sql,
                (
                    empleado.nombre,
                    empleado.correo,
                    empleado.id
                )
            )

            conexion.commit()

            return cursor.rowcount > 0

        except Exception:
            if conexion:
                conexion.rollback()
            raise

        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
        DELETE FROM empleado
        WHERE id = {marcador}
        """

        cursor.execute(sql, (id_empleado,))
        conexion.commit()

        eliminado = cursor.rowcount > 0

        conexion.close()

        return eliminado