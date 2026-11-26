import sqlite3
from typing import List
from src.negocio.models import Destination
from src.persistencia.destination_dao import DestinationDAO


def _is_integrity_error(exc: Exception) -> bool:
    return isinstance(exc, sqlite3.IntegrityError) or type(exc).__name__ == "IntegrityError"


class DestinationService:
    def __init__(self, destination_dao: DestinationDAO) -> None:
        self.destination_dao = destination_dao

    def register_destination(
        self, name: str, country: str, base_cost: float
    ) -> Destination:
        destination = Destination(name=name, country=country, base_cost=base_cost)
        destination.validate()
        try:
            return self.destination_dao.create(destination)
        except Exception as exc:
            if not _is_integrity_error(exc):
                raise
            raise ValueError(
                f"Ya existe un destino llamado '{destination.name}' en '{destination.country}'."
            ) from exc

    def get_destinations(self, include_retired: bool = False) -> List[Destination]:
        return self.destination_dao.list_all(only_active=not include_retired)

    def update_destination(
        self, destination_id: int, name: str, country: str, base_cost: float
    ) -> Destination:
        existing = self.destination_dao.get_by_id(destination_id)
        if not existing:
            raise ValueError(f"No se encontró un destino con ID {destination_id}.")

        existing.name = name
        existing.country = country
        existing.base_cost = base_cost
        existing.validate()

        try:
            self.destination_dao.update(existing)
            return existing
        except Exception as exc:
            if not _is_integrity_error(exc):
                raise
            raise ValueError(
                f"Ya existe otro destino con el nombre '{existing.name}' en '{existing.country}'."
            ) from exc

    def retire_destination(self, destination_id: int) -> Destination:
        existing = self.destination_dao.get_by_id(destination_id)
        if not existing:
            raise ValueError(f"No se encontró un destino con ID {destination_id}.")

        existing.retire()
        self.destination_dao.update(existing)
        return existing