from src.negocio.auth_service import AuthService
from src.negocio.destination_service import DestinationService
from src.negocio.package_service import PackageService
from src.negocio.reservation_service import ReservationService
from src.persistencia.conexion import DatabaseConnection
from src.persistencia.destination_dao import DestinationDAO
from src.persistencia.package_dao import PackageDAO
from src.persistencia.reservation_dao import ReservationDAO
from src.persistencia.user_dao import UserDAO
from src.presentacion.admin_cli import AdminCLI
from src.presentacion.auth_cli import AuthCLI
from src.presentacion.client_cli import ClientCLI
from src.presentacion.destination_cli import DestinationCLI
from src.presentacion.package_cli import PackageCLI


def main() -> None:
    db = DatabaseConnection()
    db.init_schema()

    user_dao = UserDAO(db)
    destination_dao = DestinationDAO(db)
    package_dao = PackageDAO(db)
    reservation_dao = ReservationDAO(db)

    auth_service = AuthService(user_dao)
    auth_service.ensure_default_admin()

    destination_service = DestinationService(destination_dao)
    package_service = PackageService(package_dao, destination_dao)
    reservation_service = ReservationService(reservation_dao, package_dao)

    auth_cli = AuthCLI(auth_service)

    while True:
        current_user = auth_cli.prompt_access()
        if not current_user:
            print("Hasta pronto.")
            break

        if current_user.role == "ADMIN":
            destination_cli = DestinationCLI(destination_service)
            package_cli = PackageCLI(package_service, destination_service)
            AdminCLI(current_user, destination_cli, package_cli, reservation_service).run()
        else:
            ClientCLI(current_user, package_service, reservation_service).run()


if __name__ == "__main__":
    main()