
from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion


class UsuarioDAO:

    @staticmethod
    def insertar(usuario):
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuario
                (nombre_usuario, password_hash, empleado_id)
                VALUES (?, ?, ?)
            """, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.empleado_id
            ))

            conexion.commit()
            return cursor.lastrowid

        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre):
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id, nombre_usuario, password_hash, empleado_id
                FROM usuario
                WHERE nombre_usuario = ?
            """, (nombre,))

            fila = cursor.fetchone()

            if fila is None:
                return None

            return Usuario(
                nombre_usuario=fila[1],
                password_hash=fila[2],
                empleado_id=fila[3],
                id=fila[0]
            )

        finally:
            conexion.close()

    @staticmethod
    def buscar_por_empleado(empleado_id):
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id, nombre_usuario, password_hash, empleado_id
                FROM usuario
                WHERE empleado_id = ?
            """, (empleado_id,))

            fila = cursor.fetchone()

            if fila is None:
                return None

            return Usuario(
                nombre_usuario=fila[1],
                password_hash=fila[2],
                empleado_id=fila[3],
                id=fila[0]
            )

        finally:
            conexion.close()
