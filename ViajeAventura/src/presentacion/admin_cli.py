from src.negocio.models import UserAccount
from src.negocio.reservation_service import ReservationService
from src.presentacion.destination_cli import DestinationCLI
from src.presentacion.package_cli import PackageCLI


class AdminCLI:
    def __init__(
        self,
        admin: UserAccount,
        destination_cli: DestinationCLI,
        package_cli: PackageCLI,
        reservation_service: ReservationService,
    ) -> None:
        self.admin = admin
        self.destination_cli = destination_cli
        self.package_cli = package_cli
        self.reservation_service = reservation_service

    def run(self) -> None:
        while True:
            print(f"\n=== PANEL ADMINISTRADOR ({self.admin.email}) ===")
            print("1. Gestión de Destinos (CRUD)")
            print("2. Gestión de Paquetes Turísticos y Salidas")
            print("3. Consultar reservas, pasajeros y estados de viaje")
            print("4. Registrar avance de etapa de un pasajero")
            print("0. Cerrar sesión")

            option = input("Seleccione una opción: ").strip()
            try:
                if option == "1":
                    self.destination_cli.run()
                elif option == "2":
                    self.package_cli.run()
                elif option == "3":
                    self._list_all_progress()
                elif option == "4":
                    self._update_stage()
                elif option == "0":
                    break
                else:
                    print("Opción inválida.")
            except ValueError as err:
                print(f"[Error] {err}")

    def _list_all_progress(self) -> None:
        reservations = self.reservation_service.get_all_reservations()
        if not reservations:
            print("No existen reservas registradas en el sistema.")
            return

        status_map = {
            "PENDING": "Pendiente",
            "IN_PROGRESS": "En curso",
            "COMPLETED": "Completada",
        }
        print("\nID Etapa | Pasajero             | Paquete              | Destino          | Estado     | Responsable")
        print("-" * 105)
        for res in reservations:
            for pax in res.passengers:
                for st in pax.stages:
                    print(
                        f"{st.id:<8} | {pax.full_name:<20} | {res.package_name:<20} | "
                        f"{st.stop_order}.{st.destination_name:<14} | "
                        f"{status_map.get(st.status, st.status):<10} | {st.updated_by_email}"
                    )

    def _update_stage(self) -> None:
        self._list_all_progress()
        stage_id = int(input("\nID Etapa a actualizar: "))
        print("Estados disponibles: 1 = Pendiente | 2 = En curso | 3 = Completada")
        choice = input("Seleccione nuevo estado: ").strip()
        mapping = {"1": "PENDING", "2": "IN_PROGRESS", "3": "COMPLETED"}
        if choice not in mapping:
            raise ValueError("Selección de estado inválida.")

        self.reservation_service.update_passenger_stage(
            stage_id=stage_id, new_status=mapping[choice], admin=self.admin
        )
        print("Avance de etapa actualizado y auditado correctamente.")