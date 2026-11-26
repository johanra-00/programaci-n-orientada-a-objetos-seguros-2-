from typing import Optional
from src.negocio.models import UserAccount
from src.persistencia.conexion import DatabaseConnection


class UserDAO:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create(self, user: UserAccount) -> UserAccount:
        sql = self.db.format_query(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)"
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (user.email, user.password_hash, user.role))
            conn.commit()
            user.id = cursor.lastrowid
            return user
        finally:
            conn.close()

    def get_by_email(self, email: str) -> Optional[UserAccount]:
        sql = self.db.format_query(
            "SELECT id, email, password_hash, role FROM users WHERE email = ?"
        )
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if not row:
                return None
            return UserAccount(
                id=row[0], email=row[1], password_hash=row[2], role=row[3]
            )
        finally:
            conn.close()