from src.negocio.destination_service import DestinationService


class DestinationCLI:
    def __init__(self, service: DestinationService) -> None:
        self.service = service

    def run(self) -> None:
        while True:
            print("\n=== VIAJES AVENTURA - GESTIÓN DE DESTINOS ===")
            print("1. Registrar nuevo destino")
            print("2. Listar destinos disponibles")
            print("3. Listar todos los destinos (incluye retirados)")
            print("4. Modificar destino")
            print("5. Retirar destino (baja lógica)")
            print("0. Volver al panel administrador")

            option = input("Seleccione una opción: ").strip()

            try:
                if option == "1":
                    self._handle_create()
                elif option == "2":
                    self._handle_list(include_retired=False)
                elif option == "3":
                    self._handle_list(include_retired=True)
                elif option == "4":
                    self._handle_update()
                elif option == "5":
                    self._handle_retire()
                elif option == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
            except ValueError as err:
                print(f"[Error de validación] {err}")
            except Exception as err:
                print(f"[Error inesperado] {err}")

    def _handle_create(self) -> None:
        name = input("Nombre del destino: ")
        country = input("País: ")
        base_cost = self._read_float("Costo base referencial: ")
        created = self.service.register_destination(name, country, base_cost)
        print(f"Destino registrado correctamente con ID {created.id}.")

    def _handle_list(self, include_retired: bool) -> None:
        destinations = self.service.get_destinations(include_retired=include_retired)
        if not destinations:
            print("No hay destinos registrados para mostrar.")
            return

        print("\nID  | Destino            | País            | Costo Base | Estado")
        print("-" * 68)
        for d in destinations:
            status = "Activo" if d.active else "Retirado"
            print(
                f"{d.id:<3} | {d.name:<18} | {d.country:<15} | ${d.base_cost:<9,.2f} | {status}"
            )

    def _handle_update(self) -> None:
        self._handle_list(include_retired=True)
        destination_id = self._read_int("\nID del destino a modificar: ")
        name = input("Nuevo nombre: ")
        country = input("Nuevo país: ")
        base_cost = self._read_float("Nuevo costo base: ")
        updated = self.service.update_destination(
            destination_id, name, country, base_cost
        )
        print(f"Destino ID {updated.id} actualizado correctamente.")

    def _handle_retire(self) -> None:
        self._handle_list(include_retired=False)
        destination_id = self._read_int("\nID del destino a retirar: ")
        retired = self.service.retire_destination(destination_id)
        print(
            f"Destino '{retired.name}' retirado. Seguirá disponible en el historial de viajes."
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