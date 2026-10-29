
import requests
import math


def mostrar_indicador():
    try:
        respuesta = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=(3, 5)
        )
        respuesta.raise_for_status()
        datos = respuesta.json()

        # Comprobar que la respuesta sea un diccionario.
        if not isinstance(datos, dict):
            raise ValueError("Respuesta inesperada.")
        # Comprobar que existan las tasas de cambio.
        tasas = datos.get("rates")
        if not isinstance(tasas, dict):
            raise ValueError("No hay valores disponibles.")

        # Validar el valor del peso chileno.
        valor = tasas.get("CLP")
        if (
            type(valor) not in (int, float)
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise ValueError("Valor del CLP inválido.")

        # Validar la fecha de actualización.
        fecha = datos.get("time_last_update_utc")
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("Fecha de actualización inválida.")

        print(f"Dólar: {valor:.2f} CLP por USD")
        print(f"Fecha de actualización: {fecha}")

    except requests.exceptions.RequestException:
        print("No pudimos consultar el servicio. Reintente.")
    except (ValueError, TypeError):
        print("La respuesta no contiene un indicador válido.")

