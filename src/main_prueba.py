import requests

def obtener_datos():
    respuesta = requests.get(
"https://open.er-api.com/v6/latest/USD",
timeout=(3, 5),
)
    print("Estado HTTP:", respuesta.status_code)
    respuesta.raise_for_status()
    return respuesta.json()



datos = obtener_datos()
print(datos)


import math

def extraer_primero(datos,moneda:str = "CLP"):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener los tipos de cambio.
    rates = datos.get("rates")

    # Verificar que rates sea un diccionario.
    if not isinstance(rates, dict):
        raise ValueError("No hay valores disponibles.")

    # Obtener el valor de la moneda especificada.
    valor = rates.get(moneda)

    # Verificar que el valor sea numérico, finito y positivo.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del CLP inválido.")

    # Obtener la fecha y devolver ambos valores.
    fecha = datos.get("time_last_update_utc")
    return valor, fecha

datos = obtener_datos()
valor1, fecha = extraer_primero(datos)

print(valor1)
print(fecha)

try:
    # Consultar la API y obtener los datos.
    datos = obtener_datos()

    # Extraer y validar la fecha y el valor del peso chileno.
    valor, fecha = extraer_primero(datos, "CLP")

    # Mostrar el valor con dos decimales.
    print(f"Dólar observado: {valor:.2f} CLP por USD")

    # Mostrar la fecha de actualización.
    print(f"Fecha de actualización: {fecha}")

except requests.exceptions.RequestException:
    print("No pudimos consultar el servicio. Reintente.")

except (ValueError, KeyError, TypeError):
    print("La respuesta no contiene un indicador válido.")