from dominio.registro_tiempo import RegistroTiempo
from persistencia.conexion import abrir_conexion, obtener_motor


class RegistroTiempoDAO:

    @staticmethod
    def _convertir(fila):
        return RegistroTiempo(
            fecha_registro=str(fila[1]),
            horas_registradas=float(fila[2]),
            id=fila[0]
        )

    @staticmethod
    def insertar(registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""
                INSERT INTO registro_tiempo
                (fecha_registro, horas_registradas)
                VALUES ({marcador}, {marcador})
            """

            cursor.execute(
                sql,
                (registro.fecha_registro, registro.horas_registradas)
            )

            registro.id = cursor.lastrowid
            conexion.commit()
            return registro
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, fecha_registro, horas_registradas "
                "FROM registro_tiempo"
            )
            return [
                RegistroTiempoDAO._convertir(fila)
                for fila in cursor.fetchall()
            ]
        finally:
            conexion.close()

    @staticmethod
    def buscar(id_registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            cursor.execute(
                f"SELECT id, fecha_registro, horas_registradas "
                f"FROM registro_tiempo WHERE id = {marcador}",
                (id_registro,)
            )

            fila = cursor.fetchone()
            if fila is None:
                return None

            return RegistroTiempoDAO._convertir(fila)
        finally:
            conexion.close()

    @staticmethod
    def actualizar(registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""
                UPDATE registro_tiempo
                SET fecha_registro = {marcador},
                    horas_registradas = {marcador}
                WHERE id = {marcador}
            """

            cursor.execute(
                sql,
                (
                    registro.fecha_registro,
                    registro.horas_registradas,
                    registro.id
                )
            )

            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            cursor.execute(
                f"DELETE FROM registro_tiempo WHERE id = {marcador}",
                (id_registro,)
            )

            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()