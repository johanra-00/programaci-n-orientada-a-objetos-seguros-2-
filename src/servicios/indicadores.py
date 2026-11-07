import requests

from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicadorDAO import IndicadorDAO


def mostrar_indicador():
    try:
        respuesta = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=(3, 5)
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        # Transformar la respuesta de la API en un objeto.
        indicador = DeserializadorIndicador.desde_api(datos)

        # Guardar el indicador en la base de datos.
        IndicadorDAO.guardar(indicador)

        print("\n--- Indicador del dólar ---")
        print(f"Valor: {indicador.valor:.2f} CLP por USD")
        print(f"Fecha: {indicador.fecha}")
        print("Origen: API")
        print("Estado: Actualizado correctamente.")

    except (
        requests.exceptions.RequestException,
        ValueError,
        TypeError
    ):
        print("\nNo se pudo consultar la API.")

        # Recuperar el último indicador guardado.
        historial = IndicadorDAO.listar()

        if historial:
            indicador = historial[0]

            print("\n--- Último indicador guardado ---")
            print(f"Valor: {indicador.valor:.2f} CLP por USD")
            print(f"Fecha: {indicador.fecha}")
            print("Origen: Base de datos")
            print("Estado: Dato recuperado localmente.")
        else:
            print("No existen indicadores guardados.")


def mostrar_historial():
    # Esta función solamente consulta la base de datos.
    historial = IndicadorDAO.listar()

    print("\n--- Historial de indicadores ---")

    if not historial:
        print("Todavía no existen registros.")
        return

    for indicador in historial:
        print("------------------------------")
        print(f"Fecha: {indicador.fecha}")
        print(f"Valor: {indicador.valor:.2f} CLP por USD")
        print(f"Fuente: {indicador.fuente}")
        print(f"Verificado: {indicador.verificado_en}")
