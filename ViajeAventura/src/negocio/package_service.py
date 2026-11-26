import sqlite3
from datetime import date
from importlib import import_module
from typing import List, Tuple

try:
    _mysql_connector = import_module("mysql.connector")
    _INTEGRITY_ERRORS = (sqlite3.IntegrityError, _mysql_connector.IntegrityError)
except ModuleNotFoundError:
    _INTEGRITY_ERRORS = (sqlite3.IntegrityError,)

from src.negocio.models import PackageDeparture, TravelPackage
from src.persistencia.destination_dao import DestinationDAO
from src.persistencia.package_dao import PackageDAO


class PackageService:
    def __init__(
        self,
        package_dao: PackageDAO,
        destination_dao: DestinationDAO,
    ) -> None:
        self.package_dao = package_dao
        self.destination_dao = destination_dao

    def create_package(
        self, name: str, ordered_destination_ids: List[Tuple[int, int]]
    ) -> TravelPackage:
        package = TravelPackage(name=name)

        for destination_id, visit_order in ordered_destination_ids:
            destination = self.destination_dao.get_by_id(destination_id)
            if not destination:
                raise ValueError(f"No existe el destino con ID {destination_id}.")
            package.add_stop(destination=destination, visit_order=visit_order)

        package.validate_itinerary()

        try:
            return self.package_dao.create_package(package)
        except _INTEGRITY_ERRORS as exc:
            raise ValueError(
                f"Ya existe un paquete turístico con el nombre '{package.name}'."
            ) from exc

    def list_packages(self) -> List[TravelPackage]:
        return self.package_dao.list_packages()

    def schedule_departure(
        self,
        package_id: int,
        start_date_str: str,
        end_date_str: str,
        price: float,
        capacity: int,
    ) -> PackageDeparture:
        package = self.package_dao.get_package_by_id(package_id)
        if not package:
            raise ValueError(f"No existe un paquete turístico con ID {package_id}.")

        package.validate_itinerary()

        try:
            start_dt = date.fromisoformat(start_date_str.strip())
            end_dt = date.fromisoformat(end_date_str.strip())
        except ValueError as exc:
            raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD.") from exc

        departure = PackageDeparture(
            package_id=package.id,
            package_name=package.name,
            start_date=start_dt,
            end_date=end_dt,
            price=price,
            capacity=capacity,
        )
        departure.validate()
        return self.package_dao.create_departure(departure)

    def list_departures(self) -> List[PackageDeparture]:
        return self.package_dao.list_departures()