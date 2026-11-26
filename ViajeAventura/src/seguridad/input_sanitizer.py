import math
import re


class InputSanitizer:
    # Characters and sequences never allowed in standard text fields
    FORBIDDEN_SEQUENCES = (
        "@", "|", ";", "--", "/*", "*/", ".-.", "..",
        "<", ">", "\\", "\"", "'", "`", "$", "=", "{", "}", "[", "]"
    )

    # Letters (including Spanish accents and ñ) + single spaces between words
    PERSON_NAME_REGEX = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"
    )

    # Letters + single spaces (no numbers or symbols)
    COUNTRY_REGEX = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"
    )

    # Letters + single spaces or single hyphens (e.g., "Viña del Mar", "San José")
    DESTINATION_NAME_REGEX = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?:[ -][A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"
    )

    # Letters, numbers, single spaces or single hyphens (e.g., "Ruta Andina 2026")
    PACKAGE_NAME_REGEX = re.compile(
        r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+(?:[ -][A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+)*$"
    )

    # Chilean RUT (12345678-9 or 12.345.678-K) or alphanumeric passport (5 to 15 chars)
    DOCUMENT_ID_REGEX = re.compile(
        r"^(?:\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]|\d{7,8}-[0-9Kk]|[A-Z0-9]{5,15})$"
    )

    # Strict email format without consecutive dots or forbidden symbols
    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
    )

    @classmethod
    def _normalize_whitespace(cls, raw_value: str, field_label: str) -> str:
        if raw_value is None or not isinstance(raw_value, str):
            raise ValueError(f"El campo '{field_label}' es obligatorio.")
        cleaned = re.sub(r"[\x00-\x1f\x7f]", "", raw_value).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if not cleaned:
            raise ValueError(f"El campo '{field_label}' no puede estar vacío.")
        return cleaned

    @classmethod
    def _reject_forbidden_sequences(cls, value: str, field_label: str) -> None:
        for seq in cls.FORBIDDEN_SEQUENCES:
            if seq in value:
                raise ValueError(
                    f"El campo '{field_label}' contiene caracteres o símbolos no permitidos ('{seq}')."
                )

    @classmethod
    def sanitize_person_name(cls, raw_name: str, field_label: str = "Nombre completo") -> str:
        cleaned = cls._normalize_whitespace(raw_name, field_label)
        cls._reject_forbidden_sequences(cleaned, field_label)
        if len(cleaned) < 2 or len(cleaned) > 120:
            raise ValueError(f"El campo '{field_label}' debe tener entre 2 y 120 caracteres.")
        if not cls.PERSON_NAME_REGEX.match(cleaned):
            raise ValueError(
                f"El campo '{field_label}' solo puede contener letras y espacios (sin números ni símbolos)."
            )
        return cleaned

    @classmethod
    def sanitize_country(cls, raw_country: str) -> str:
        cleaned = cls._normalize_whitespace(raw_country, "País")
        cls._reject_forbidden_sequences(cleaned, "País")
        if len(cleaned) < 2 or len(cleaned) > 80:
            raise ValueError("El país debe tener entre 2 y 80 caracteres.")
        if not cls.COUNTRY_REGEX.match(cleaned):
            raise ValueError(
                "El país solo puede contener letras y espacios (sin números ni símbolos)."
            )
        return cleaned

    @classmethod
    def sanitize_destination_name(cls, raw_name: str) -> str:
        cleaned = cls._normalize_whitespace(raw_name, "Nombre del destino")
        cls._reject_forbidden_sequences(cleaned, "Nombre del destino")
        if len(cleaned) < 2 or len(cleaned) > 100:
            raise ValueError("El nombre del destino debe tener entre 2 y 100 caracteres.")
        if not cls.DESTINATION_NAME_REGEX.match(cleaned):
            raise ValueError(
                "El nombre del destino solo permite letras, espacios y guiones simples (sin números, '@', '|' ni símbolos)."
            )
        return cleaned

    @classmethod
    def sanitize_package_name(cls, raw_name: str) -> str:
        cleaned = cls._normalize_whitespace(raw_name, "Nombre del paquete")
        cls._reject_forbidden_sequences(cleaned, "Nombre del paquete")
        if len(cleaned) < 3 or len(cleaned) > 120:
            raise ValueError("El nombre del paquete debe tener entre 3 y 120 caracteres.")
        if not cls.PACKAGE_NAME_REGEX.match(cleaned):
            raise ValueError(
                "El nombre del paquete solo permite letras, números, espacios y guiones simples."
            )
        return cleaned

    @classmethod
    def sanitize_document_id(cls, raw_doc: str) -> str:
        cleaned = cls._normalize_whitespace(raw_doc, "Documento de identidad").upper()
        if " " in cleaned:
            raise ValueError("El documento de identidad no debe contener espacios.")
        if not cls.DOCUMENT_ID_REGEX.match(cleaned):
            raise ValueError(
                "Formato de RUT o Pasaporte inválido (ejemplo válido: 12345678-9 o AB123456)."
            )
        return cleaned

    @classmethod
    def sanitize_email(cls, raw_email: str) -> str:
        cleaned = cls._normalize_whitespace(raw_email, "Correo electrónico").lower()
        forbidden_in_email = tuple(s for s in cls.FORBIDDEN_SEQUENCES if s != "@")
        for seq in forbidden_in_email:
            if seq in cleaned:
                raise ValueError(
                    f"El correo electrónico contiene caracteres o secuencias no permitidas ('{seq}')."
                )
        if " " in cleaned or not cls.EMAIL_REGEX.match(cleaned) or len(cleaned) > 150:
            raise ValueError("El formato del correo electrónico no es válido.")
        return cleaned

    @classmethod
    def sanitize_money(cls, value: float, field_label: str = "Monto") -> float:
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"El campo '{field_label}' debe ser un número válido.")
        if value < 0:
            raise ValueError(f"El campo '{field_label}' no puede ser negativo.")
        return round(float(value), 2)

    @classmethod
    def sanitize_positive_int(cls, value: int, field_label: str = "Cantidad") -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"El campo '{field_label}' debe ser un número entero mayor a cero.")
        return value