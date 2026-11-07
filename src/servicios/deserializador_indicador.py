
from datetime import datetime
from dominio.indicador import Indicador


class DeserializadorIndicador:

    @staticmethod
    def desde_api(datos):
        if not isinstance(datos, dict):
            raise ValueError("Respuesta de API inválida.")

        tasas = datos.get("rates")

        if not isinstance(tasas, dict):
            raise ValueError("No se encontraron las tasas.")

        valor = tasas.get("CLP")
        fecha_api = datos.get("time_last_update_utc")

        if not isinstance(fecha_api, str):
            raise ValueError("Fecha de API inválida.")

        try:
            fecha = datetime.strptime(
                fecha_api, "%a, %d %b %Y %H:%M:%S %z"
            ).date().isoformat()
        except ValueError:
            raise ValueError("No se pudo interpretar la fecha.")

        return Indicador(
            fecha=fecha,
            valor=valor
        )
