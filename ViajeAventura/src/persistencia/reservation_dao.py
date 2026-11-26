from datetime import datetime
from typing import List, Optional
from src.negocio.models import Passenger, Reservation, StageProgress
from src.persistencia.conexion import DatabaseConnection


class ReservationDAO:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create_reservation(
        self, reservation: Reservation, stop_ids: List[int]
    ) -> Reservation:
        res_sql = self.db.format_query(
            """
            INSERT INTO reservations
                (user_id, departure_id, created_at, unit_price, total_price, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        )
        pax_sql = self.db.format_query(
            """
            INSERT INTO passengers (reservation_id, full_name, document_id)
            VALUES (?, ?, ?)
            """
        )
        stage_sql = self.db.format_query(
            """
            INSERT INTO stage_progress
                (passenger_id, stop_id, status, updated_at, updated_by)
            VALUES (?, ?, 'PENDING', ?, ?)
            """
        )

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            now_str = reservation.created_at.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                res_sql,
                (
                    reservation.user_id,
                    reservation.departure_id,
                    now_str,
                    reservation.unit_price,
                    reservation.total_price,
                    reservation.status,
                ),
            )
            reservation.id = cursor.lastrowid

            for passenger in reservation.passengers:
                cursor.execute(
                    pax_sql,
                    (reservation.id, passenger.full_name, passenger.document_id),
                )
                passenger.id = cursor.lastrowid

                for stop_id in stop_ids:
                    cursor.execute(
                        stage_sql,
                        (passenger.id, stop_id, now_str, reservation.user_id),
                    )

            conn.commit()
            return reservation
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def list_by_user(self, user_id: int) -> List[Reservation]:
        return self._fetch_reservations(user_id=user_id)

    def list_all(self) -> List[Reservation]:
        return self._fetch_reservations(user_id=None)

    def _fetch_reservations(self, user_id: Optional[int]) -> List[Reservation]:
        base_sql = """
            SELECT
                r.id, r.user_id, u.email, r.departure_id,
                tp.name, pd.start_date, pd.end_date,
                r.created_at, r.unit_price, r.total_price, r.status
            FROM reservations r
            JOIN users u ON u.id = r.user_id
            JOIN package_departures pd ON pd.id = r.departure_id
            JOIN travel_packages tp ON tp.id = pd.package_id
        """
        params = ()
        if user_id is not None:
            base_sql += " WHERE r.user_id = ?"
            params = (user_id,)
        base_sql += " ORDER BY r.id DESC"

        res_sql = self.db.format_query(base_sql)
        pax_sql = self.db.format_query(
            "SELECT id, full_name, document_id FROM passengers WHERE reservation_id = ?"
        )
        stages_sql = self.db.format_query(
            """
            SELECT
                sp.id, sp.stop_id, s.visit_order, d.name,
                sp.status, sp.updated_at, u.email
            FROM stage_progress sp
            JOIN itinerary_stops s ON s.id = sp.stop_id
            JOIN destinations d ON d.id = s.destination_id
            JOIN users u ON u.id = sp.updated_by
            WHERE sp.passenger_id = ?
            ORDER BY s.visit_order ASC
            """
        )

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(res_sql, params)
            res_rows = cursor.fetchall()

            reservations: List[Reservation] = []
            for r in res_rows:
                cursor.execute(pax_sql, (r[0],))
                pax_rows = cursor.fetchall()

                passengers: List[Passenger] = []
                for p in pax_rows:
                    cursor.execute(stages_sql, (p[0],))
                    st_rows = cursor.fetchall()
                    stages = [
                        StageProgress(
                            id=st[0],
                            stop_id=st[1],
                            stop_order=st[2],
                            destination_name=st[3],
                            status=st[4],
                            updated_at=(
                                st[5]
                                if isinstance(st[5], datetime)
                                else datetime.fromisoformat(str(st[5]))
                            ),
                            updated_by_email=st[6],
                        )
                        for st in st_rows
                    ]
                    passengers.append(
                        Passenger(
                            id=p[0],
                            full_name=p[1],
                            document_id=p[2],
                            stages=stages,
                        )
                    )

                created_val = (
                    r[7]
                    if isinstance(r[7], datetime)
                    else datetime.fromisoformat(str(r[7]))
                )
                reservations.append(
                    Reservation(
                        id=r[0],
                        user_id=r[1],
                        user_email=r[2],
                        departure_id=r[3],
                        package_name=r[4],
                        start_date=str(r[5]),
                        end_date=str(r[6]),
                        created_at=created_val,
                        unit_price=float(r[8]),
                        total_price=float(r[9]),
                        status=r[10],
                        passengers=passengers,
                    )
                )
            return reservations
        finally:
            conn.close()

    def update_stage_status(
        self, stage_id: int, status: str, admin_id: int
    ) -> bool:
        sql = self.db.format_query(
            """
            UPDATE stage_progress
            SET status = ?, updated_at = ?, updated_by = ?
            WHERE id = ?
            """
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(sql, (status, now_str, admin_id, stage_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()