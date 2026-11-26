import os
import sqlite3
from importlib import import_module

try:
    load_dotenv = import_module("dotenv").load_dotenv
except ModuleNotFoundError:
    def load_dotenv() -> bool:
        return False

load_dotenv()


class DatabaseConnection:
    def __init__(self) -> None:
        self.engine = os.getenv("DB_ENGINE", "sqlite").lower().strip()
        if self.engine not in ("sqlite", "mysql"):
            raise ValueError(f"Unsupported database engine: {self.engine}")

    def get_connection(self):
        if self.engine == "sqlite":
            db_path = os.getenv("SQLITE_PATH", "src/ViajeAventura.DB")
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

        mysql_connector = import_module("mysql.connector")
        return mysql_connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "viajes_aventura"),
        )

    def format_query(self, query: str) -> str:
        """Converts SQLite placeholders (?) to MySQL placeholders (%s)."""
        if self.engine == "mysql":
            return query.replace("?", "%s")
        return query

    def init_schema(self) -> None:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if self.engine == "sqlite":
                statements = [
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'CLIENT'
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS destinations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        country TEXT NOT NULL,
                        base_cost REAL NOT NULL CHECK (base_cost >= 0),
                        active INTEGER NOT NULL DEFAULT 1,
                        UNIQUE(name, country)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS travel_packages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        active INTEGER NOT NULL DEFAULT 1
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS itinerary_stops (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        package_id INTEGER NOT NULL,
                        destination_id INTEGER NOT NULL,
                        visit_order INTEGER NOT NULL CHECK (visit_order >= 1),
                        UNIQUE(package_id, visit_order),
                        FOREIGN KEY (package_id) REFERENCES travel_packages(id),
                        FOREIGN KEY (destination_id) REFERENCES destinations(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS package_departures (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        package_id INTEGER NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        price REAL NOT NULL CHECK (price >= 0),
                        capacity INTEGER NOT NULL CHECK (capacity > 0),
                        FOREIGN KEY (package_id) REFERENCES travel_packages(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS reservations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        departure_id INTEGER NOT NULL,
                        created_at TEXT NOT NULL,
                        unit_price REAL NOT NULL CHECK (unit_price >= 0),
                        total_price REAL NOT NULL CHECK (total_price >= 0),
                        status TEXT NOT NULL DEFAULT 'CONFIRMED',
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (departure_id) REFERENCES package_departures(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS passengers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        reservation_id INTEGER NOT NULL,
                        full_name TEXT NOT NULL,
                        document_id TEXT NOT NULL,
                        FOREIGN KEY (reservation_id) REFERENCES reservations(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS stage_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        passenger_id INTEGER NOT NULL,
                        stop_id INTEGER NOT NULL,
                        status TEXT NOT NULL DEFAULT 'PENDING',
                        updated_at TEXT NOT NULL,
                        updated_by INTEGER NOT NULL,
                        UNIQUE(passenger_id, stop_id),
                        FOREIGN KEY (passenger_id) REFERENCES passengers(id),
                        FOREIGN KEY (stop_id) REFERENCES itinerary_stops(id),
                        FOREIGN KEY (updated_by) REFERENCES users(id)
                    );
                    """,
                ]
            else:
                statements = [
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(150) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        role VARCHAR(20) NOT NULL DEFAULT 'CLIENT'
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS destinations (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(120) NOT NULL,
                        country VARCHAR(120) NOT NULL,
                        base_cost DECIMAL(10, 2) NOT NULL,
                        active TINYINT(1) NOT NULL DEFAULT 1,
                        UNIQUE KEY uq_destination_name_country (name, country)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS travel_packages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(150) NOT NULL UNIQUE,
                        active TINYINT(1) NOT NULL DEFAULT 1
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS itinerary_stops (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        package_id INT NOT NULL,
                        destination_id INT NOT NULL,
                        visit_order INT NOT NULL,
                        UNIQUE KEY uq_package_order (package_id, visit_order),
                        FOREIGN KEY (package_id) REFERENCES travel_packages(id),
                        FOREIGN KEY (destination_id) REFERENCES destinations(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS package_departures (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        package_id INT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        price DECIMAL(10, 2) NOT NULL,
                        capacity INT NOT NULL,
                        FOREIGN KEY (package_id) REFERENCES travel_packages(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS reservations (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        departure_id INT NOT NULL,
                        created_at DATETIME NOT NULL,
                        unit_price DECIMAL(10, 2) NOT NULL,
                        total_price DECIMAL(10, 2) NOT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (departure_id) REFERENCES package_departures(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS passengers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        reservation_id INT NOT NULL,
                        full_name VARCHAR(150) NOT NULL,
                        document_id VARCHAR(50) NOT NULL,
                        FOREIGN KEY (reservation_id) REFERENCES reservations(id)
                    );
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS stage_progress (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        passenger_id INT NOT NULL,
                        stop_id INT NOT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
                        updated_at DATETIME NOT NULL,
                        updated_by INT NOT NULL,
                        UNIQUE KEY uq_passenger_stop (passenger_id, stop_id),
                        FOREIGN KEY (passenger_id) REFERENCES passengers(id),
                        FOREIGN KEY (stop_id) REFERENCES itinerary_stops(id),
                        FOREIGN KEY (updated_by) REFERENCES users(id)
                    );
                    """,
                ]

            for stmt in statements:
                cursor.execute(stmt)
            conn.commit()
        finally:
            conn.close()