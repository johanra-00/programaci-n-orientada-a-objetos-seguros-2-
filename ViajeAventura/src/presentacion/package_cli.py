from typing import List, Tuple
from src.negocio.destination_service import DestinationService
from src.negocio.package_service import PackageService


class PackageCLI:
    def __init__(
        self,
        package_service: PackageService,
        destination_service: DestinationService,
    ) -> None:
        self.package_service = package_service
        self.destination_service = destination_service

    def run(self) -> None:
        while True:
            print("\n=== VIAJES AVENTURA - PAQUETES TURÍSTICOS Y SALIDAS ===")
            print("1. Crear paquete turístico (combinar destinos)")
            print("2. Listar paquetes turísticos e itinerarios")
            print("3. Programar fecha de salida (fechas, precio y cupos)")
            print("4. Consultar salidas y disponibilidad de cupos")
            print("0. Volver al panel administrador")

            option = input("Seleccione una opción: ").strip()

            try:
                if option == "1":
                    self._handle_create_package()
                elif option == "2":
                    self._handle_list_packages()
                elif option == "3":
                    self._handle_schedule_departure()
                elif option == "4":
                    self._handle_list_departures()
                elif option == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
            except ValueError as err:
                print(f"[Error de validación] {err}")
            except Exception as err:
                print(f"[Error inesperado] {err}")

    def _handle_create_package(self) -> None:
        destinations = self.destination_service.get_destinations(include_retired=False)
        if len(destinations) < 2:
            print("Debe registrar al menos 2 destinos activos antes de crear un paquete.")
            return

        print("\nDestinos disponibles:")
        print("ID  | Destino            | País            | Costo Base")
        print("-" * 58)
        for d in destinations:
            print(f"{d.id:<3} | {d.name:<18} | {d.country:<15} | ${d.base_cost:,.2f}")

        name = input("\nNombre del nuevo paquete turístico: ")
        count = self._read_int("¿Cuántos destinos tendrá el itinerario? (mínimo 2): ")

        stops_input: List[Tuple[int, int]] = []
        for order in range(1, count + 1):
            dest_id = self._read_int(f"  ID del destino para la etapa #{order}: ")
            stops_input.append((dest_id, order))

        created = self.package_service.create_package(name, stops_input)
        print(
            f"Paquete '{created.name}' creado con ID {created.id}. "
            f"Costo base calculado: ${created.calculate_base_cost():,.2f}"
        )

    def _handle_list_packages(self) -> None:
        packages = self.package_service.list_packages()
        if not packages:
            print("No hay paquetes turísticos registrados.")
            return

        print("\nID  | Paquete Turístico        | Itinerario (Orden de visita)           | Costo Base")
        print("-" * 88)
        for pkg in packages:
            route = " -> ".join(
                f"{s.visit_order}.{s.destination.name}" for s in pkg.stops
            )
            print(
                f"{pkg.id:<3} | {pkg.name:<24} | {route:<40} | ${pkg.calculate_base_cost():,.2f}"
            )

    def _handle_schedule_departure(self) -> None:
        self._handle_list_packages()
        package_id = self._read_int("\nID del paquete turístico a programar: ")
        start_date = input("Fecha de inicio (AAAA-MM-DD): ")
        end_date = input("Fecha de término (AAAA-MM-DD): ")
        price = self._read_float("Precio por pasajero: ")
        capacity = self._read_int("Cantidad de cupos disponibles: ")

        departure = self.package_service.schedule_departure(
            package_id=package_id,
            start_date_str=start_date,
            end_date_str=end_date,
            price=price,
            capacity=capacity,
        )
        print(
            f"Salida ID {departure.id} programada para '{departure.package_name}' "
            f"({departure.start_date} al {departure.end_date})."
        )

    def _handle_list_departures(self) -> None:
        departures = self.package_service.list_departures()
        if not departures:
            print("No hay fechas de salida programadas.")
            return

        print(
            "\nID  | Paquete Turístico        | Inicio     | Fin        | Precio     | Cupos | Estado"
        )
        print("-" * 92)
        for dep in departures:
            avail = dep.available_seats()
            status = f"{avail}/{dep.capacity} disp." if avail > 0 else "Agotado"
            print(
                f"{dep.id:<3} | {dep.package_name:<24} | {dep.start_date} | "
                f"{dep.end_date} | ${dep.price:<9,.2f} | {dep.capacity:<5} | {status}"
            )

    @staticmethod
    def _read_int(prompt: str) -> int:
        try:
            return int(input(prompt).strip())
        except ValueError as exc:
            raise ValueError("Debe ingresar un número entero válido.") from exc

    @staticmethod
    def _read_float(prompt: str) -> float:
        try:
            return float(input(prompt).strip())
        except ValueError as exc:
            raise ValueError("Debe ingresar un monto numérico válido.") from exc