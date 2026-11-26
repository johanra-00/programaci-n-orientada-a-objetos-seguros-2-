from typing import List, Optional
from src.negocio.models import Destination
from src.persistencia.conexion import DatabaseConnection


class DestinationDAO:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create(self, destination: Destination) -> Destination:
        query = self.db.format_query(
            """
            INSERT INTO destinations (name, country, base_cost, active)
            VALUES (?, ?, ?, ?)
            """
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    destination.name,
                    destination.country,
                    destination.base_cost,
                    1 if destination.active else 0,
                ),
            )
            conn.commit()
            destination.id = cursor.lastrowid
            return destination
        finally:
            conn.close()

    def get_by_id(self, destination_id: int) -> Optional[Destination]:
        query = self.db.format_query(
            """
            SELECT id, name, country, base_cost, active
            FROM destinations
            WHERE id = ?
            """
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (destination_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Destination(
                id=row[0],
                name=row[1],
                country=row[2],
                base_cost=float(row[3]),
                active=bool(row[4]),
            )
        finally:
            conn.close()

    def list_all(self, only_active: bool = True) -> List[Destination]:
        base_sql = "SELECT id, name, country, base_cost, active FROM destinations"
        if only_active:
            base_sql += " WHERE active = 1"
        base_sql += " ORDER BY id ASC"

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(base_sql)
            rows = cursor.fetchall()
            return [
                Destination(
                    id=row[0],
                    name=row[1],
                    country=row[2],
                    base_cost=float(row[3]),
                    active=bool(row[4]),
                )
                for row in rows
            ]
        finally:
            conn.close()

    def update(self, destination: Destination) -> bool:
        query = self.db.format_query(
            """
            UPDATE destinations
            SET name = ?, country = ?, base_cost = ?, active = ?
            WHERE id = ?
            """
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    destination.name,
                    destination.country,
                    destination.base_cost,
                    1 if destination.active else 0,
                    destination.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()