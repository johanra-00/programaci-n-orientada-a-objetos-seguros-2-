
from datetime import date, datetime
import math


class Indicador:

    def __init__(
        self,
        fecha,
        valor,
        verificado_en=None,
        fuente="api_dolar_curso"
    ):
        if not isinstance(fecha, str):
            raise TypeError("La fecha debe ser texto.")

        try:
            date.fromisoformat(fecha)
        except ValueError:
            raise ValueError("La fecha debe tener formato ISO.")

        if (
            type(valor) not in (int, float)
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise ValueError("El valor debe ser positivo.")

        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = (
            verificado_en or datetime.now().isoformat(timespec="seconds")
        )
