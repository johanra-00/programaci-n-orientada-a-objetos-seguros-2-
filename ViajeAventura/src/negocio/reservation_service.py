from typing import List, Tuple
from src.negocio.models import Passenger, Reservation, UserAccount
from src.persistencia.package_dao import PackageDAO
from src.persistencia.reservation_dao import ReservationDAO


class ReservationService:
    def __init__(
        self,
        reservation_dao: ReservationDAO,
        package_dao: PackageDAO,
    ) -> None:
        self.reservation_dao = reservation_dao
        self.package_dao = package_dao

    def create_reservation(
        self,
        user: UserAccount,
        departure_id: int,
        passengers_data: List[Tuple[str, str]],
    ) -> Reservation:
        if not passengers_data:
            raise ValueError("Debe ingresar al menos un pasajero para la reserva.")

        departures = self.package_dao.list_departures()
        departure = next((d for d in departures if d.id == departure_id), None)
        if not departure:
            raise ValueError(f"No existe la salida con ID {departure_id}.")

        available = departure.available_seats()
        if len(passengers_data) > available:
            raise ValueError(
                f"Cupos insuficientes. Solicitados: {len(passengers_data)}, disponibles: {available}."
            )

        package = self.package_dao.get_package_by_id(departure.package_id)
        if not package:
            raise ValueError("No se encontró el paquete asociado a la salida.")

        passengers: List[Passenger] = []
        for full_name, document_id in passengers_data:
            p = Passenger(full_name=full_name, document_id=document_id)
            p.validate()
            passengers.append(p)

        reservation = Reservation(
            user_id=user.id,
            departure_id=departure.id,
            unit_price=departure.price,
            passengers=passengers,
            package_name=package.name,
            start_date=departure.start_date.isoformat(),
            end_date=departure.end_date.isoformat(),
        )
        reservation.confirm()

        stop_ids = [stop.id for stop in package.stops]
        return self.reservation_dao.create_reservation(reservation, stop_ids)

    def get_user_history(self, user_id: int) -> List[Reservation]:
        return self.reservation_dao.list_by_user(user_id)

    def get_all_reservations(self) -> List[Reservation]:
        return self.reservation_dao.list_all()

    def update_passenger_stage(
        self, stage_id: int, new_status: str, admin: UserAccount
    ) -> None:
        if admin.role != "ADMIN":
            raise ValueError("Acceso denegado: se requiere rol de administrador.")
        if new_status not in ("PENDING", "IN_PROGRESS", "COMPLETED"):
            raise ValueError("Estado inválido. Use PENDING, IN_PROGRESS o COMPLETED.")
        updated = self.reservation_dao.update_stage_status(
            stage_id=stage_id, status=new_status, admin_id=admin.id
        )
        if not updated:
            raise ValueError(f"No se encontró el registro de etapa con ID {stage_id}.")