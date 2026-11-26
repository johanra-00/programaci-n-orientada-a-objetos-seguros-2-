from typing import List, Tuple
from src.negocio.models import UserAccount
from src.negocio.package_service import PackageService
from src.negocio.reservation_service import ReservationService


class ClientCLI:
    def __init__(
        self,
        user: UserAccount,
        package_service: PackageService,
        reservation_service: ReservationService,
    ) -> None:
        self.user = user
        self.package_service = package_service
        self.reservation_service = reservation_service

    def run(self) -> None:
        while True:
            print(f"\n=== MENÚ CLIENTE ({self.user.email}) ===")
            print("1. Consultar salidas y cupos disponibles")
            print("2. Realizar reserva de paquete turístico")
            print("3. Consultar historial de reservas y avance de viaje")
            print("0. Cerrar sesión")

            option = input("Seleccione una opción: ").strip()
            try:
                if option == "1":
                    self._show_departures()
                elif option == "2":
                    self._create_reservation()
                elif option == "3":
                    self._show_history()
                elif option == "0":
                    break
                else:
                    print("Opción inválida.")
            except ValueError as err:
                print(f"[Error] {err}")

    def _show_departures(self) -> None:
        departures = self.package_service.list_departures()
        if not departures:
            print("No hay salidas programadas actualmente.")
            return

        print("\nID  | Paquete Turístico        | Inicio     | Fin        | Precio     | Disponibles")
        print("-" * 88)
        for d in departures:
            print(
                f"{d.id:<3} | {d.package_name:<24} | {d.start_date} | "
                f"{d.end_date} | ${d.price:<9,.2f} | {d.available_seats()}/{d.capacity}"
            )

    def _create_reservation(self) -> None:
        self._show_departures()
        departure_id = int(input("\nID de la salida que desea reservar: "))
        count = int(input("Cantidad de pasajeros: "))

        passengers: List[Tuple[str, str]] = []
        for idx in range(1, count + 1):
            print(f"Datos del pasajero #{idx}:")
            full_name = input("  Nombre completo: ")
            document_id = input("  RUT o Pasaporte: ")
            passengers.append((full_name, document_id))

        res = self.reservation_service.create_reservation(
            user=self.user,
            departure_id=departure_id,
            passengers_data=passengers,
        )
        print(
            f"Reserva ID {res.id} confirmada para '{res.package_name}'. "
            f"Total contratado: ${res.total_price:,.2f} ({len(res.passengers)} pasajero(s))."
        )

    def _show_history(self) -> None:
        history = self.reservation_service.get_user_history(self.user.id)
        if not history:
            print("Aún no tiene reservas registradas.")
            return

        status_map = {
            "PENDING": "Pendiente",
            "IN_PROGRESS": "En curso",
            "COMPLETED": "Completada",
        }
        for res in history:
            print(
                f"\nReserva #{res.id} | Paquete: {res.package_name} "
                f"({res.start_date} al {res.end_date}) | Total: ${res.total_price:,.2f} | Estado: {res.status}"
            )
            for pax in res.passengers:
                print(
                    f"  - Pasajero: {pax.full_name} ({pax.document_id}) -> Estado general: {pax.get_trip_status()}"
                )
                for st in pax.stages:
                    label = status_map.get(st.status, st.status)
                    print(
                        f"      Etapa {st.stop_order}: {st.destination_name} [{label}] "
                        f"(Actualizado: {st.updated_at.strftime('%Y-%m-%d %H:%M')})"
                    )