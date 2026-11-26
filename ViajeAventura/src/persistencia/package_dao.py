from datetime import date
from typing import List, Optional
from src.negocio.models import (
    Destination,
    ItineraryStop,
    PackageDeparture,
    TravelPackage,
)
from src.persistencia.conexion import DatabaseConnection


class PackageDAO:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create_package(self, package: TravelPackage) -> TravelPackage:
        pkg_sql = self.db.format_query(
            "INSERT INTO travel_packages (name, active) VALUES (?, ?)"
        )
        stop_sql = self.db.format_query(
            """
            INSERT INTO itinerary_stops (package_id, destination_id, visit_order)
            VALUES (?, ?, ?)
            """
        )

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(pkg_sql, (package.name, 1 if package.active else 0))
            package.id = cursor.lastrowid

            for stop in package.stops:
                cursor.execute(
                    stop_sql,
                    (package.id, stop.destination.id, stop.visit_order),
                )
                stop.id = cursor.lastrowid

            conn.commit()
            return package
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_package_by_id(self, package_id: int) -> Optional[TravelPackage]:
        pkg_sql = self.db.format_query(
            "SELECT id, name, active FROM travel_packages WHERE id = ?"
        )
        stops_sql = self.db.format_query(
            """
            SELECT s.id, s.visit_order, d.id, d.name, d.country, d.base_cost, d.active
            FROM itinerary_stops s
            JOIN destinations d ON d.id = s.destination_id
            WHERE s.package_id = ?
            ORDER BY s.visit_order ASC
            """
        )

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(pkg_sql, (package_id,))
            pkg_row = cursor.fetchone()
            if not pkg_row:
                return None

            cursor.execute(stops_sql, (package_id,))
            stop_rows = cursor.fetchall()
            stops = [
                ItineraryStop(
                    id=row[0],
                    visit_order=row[1],
                    destination=Destination(
                        id=row[2],
                        name=row[3],
                        country=row[4],
                        base_cost=float(row[5]),
                        active=bool(row[6]),
                    ),
                )
                for row in stop_rows
            ]

            return TravelPackage(
                id=pkg_row[0],
                name=pkg_row[1],
                active=bool(pkg_row[2]),
                stops=stops,
            )
        finally:
            conn.close()

    def list_packages(self) -> List[TravelPackage]:
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM travel_packages ORDER BY id ASC")
            package_ids = [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

        packages: List[TravelPackage] = []
        for pid in package_ids:
            pkg = self.get_package_by_id(pid)
            if pkg:
                packages.append(pkg)
        return packages

    def create_departure(self, departure: PackageDeparture) -> PackageDeparture:
        sql = self.db.format_query(
            """
            INSERT INTO package_departures (package_id, start_date, end_date, price, capacity)
            VALUES (?, ?, ?, ?, ?)
            """
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    departure.package_id,
                    departure.start_date.isoformat(),
                    departure.end_date.isoformat(),
                    departure.price,
                    departure.capacity,
                ),
            )
            conn.commit()
            departure.id = cursor.lastrowid
            return departure
        finally:
            conn.close()

    def list_departures(self) -> List[PackageDeparture]:
        sql = """
            SELECT
                pd.id,
                pd.package_id,
                tp.name,
                pd.start_date,
                pd.end_date,
                pd.price,
                pd.capacity,
                COALESCE(COUNT(p.id), 0) AS booked_seats
            FROM package_departures pd
            JOIN travel_packages tp ON tp.id = pd.package_id
            LEFT JOIN reservations r
                ON r.departure_id = pd.id AND r.status = 'CONFIRMED'
            LEFT JOIN passengers p
                ON p.reservation_id = r.id
            GROUP BY
                pd.id, pd.package_id, tp.name,
                pd.start_date, pd.end_date, pd.price, pd.capacity
            ORDER BY pd.start_date ASC, pd.id ASC
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            departures: List[PackageDeparture] = []
            for row in rows:
                start_val = (
                    row[3]
                    if isinstance(row[3], date)
                    else date.fromisoformat(str(row[3]))
                )
                end_val = (
                    row[4]
                    if isinstance(row[4], date)
                    else date.fromisoformat(str(row[4]))
                )
                departures.append(
                    PackageDeparture(
                        id=row[0],
                        package_id=row[1],
                        package_name=row[2],
                        start_date=start_val,
                        end_date=end_val,
                        price=float(row[5]),
                        capacity=int(row[6]),
                        booked_seats=int(row[7]),
                    )
                )
            return departures
        finally:
            conn.close()