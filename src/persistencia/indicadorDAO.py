
from persistencia.conexion import abrir_conexion
from dominio.indicador import Indicador


class IndicadorDAO:

    @staticmethod
    def guardar(indicador):
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO indicador_api
                (fuente, codigo, fecha, valor, unidad, verificado_en)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (fuente, codigo, fecha)
                DO UPDATE SET
                    valor = excluded.valor,
                    unidad = excluded.unidad,
                    verificado_en = excluded.verificado_en
            """, (
                indicador.fuente,
                indicador.codigo,
                indicador.fecha,
                indicador.valor,
                indicador.unidad,
                indicador.verificado_en
            ))

            conexion.commit()
            return True

        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT fecha, valor, verificado_en, fuente
                FROM indicador_api
                WHERE codigo = ?
                ORDER BY fecha DESC
            """, ("dolar",))

            filas = cursor.fetchall()

            return [
                Indicador(
                    fecha=fila[0],
                    valor=fila[1],
                    verificado_en=fila[2],
                    fuente=fila[3]
                )
                for fila in filas
            ]

        finally:
            conexion.close()
