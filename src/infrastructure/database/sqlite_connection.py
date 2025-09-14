"""
SQLite database connection and schema setup
"""

import sqlite3
from pathlib import Path
from typing import Optional


class SQLiteConnection:
    """Manages SQLite database connection and schema"""

    def __init__(self, db_path: str = "data/biblioteca.db"):
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = Path(self.db_path).parent
        data_dir.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection, create if not exists"""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._initialize_schema()
        return self._connection

    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def _initialize_schema(self):
        """Initialize database schema"""
        cursor = self._connection.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                numero_identificacion TEXT UNIQUE NOT NULL,
                telefono TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Library items table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items_biblioteca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT,
                isbn TEXT,
                categoria TEXT NOT NULL,
                estado TEXT DEFAULT 'disponible',
                descripcion TEXT,
                ubicacion TEXT,
                fecha_adquisicion DATETIME DEFAULT CURRENT_TIMESTAMP,
                valor_reposicion REAL
            )
        """
        )

        # Employees table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                usuario_sistema TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                cargo TEXT DEFAULT 'Bibliotecario',
                turno TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Loans table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                empleado_id INTEGER NOT NULL,
                fecha_prestamo DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_devolucion_esperada DATETIME NOT NULL,
                fecha_devolucion_real DATETIME,
                observaciones TEXT,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (item_id) REFERENCES items_biblioteca (id),
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """
        )

        # Reservations table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                empleado_id INTEGER NOT NULL,
                fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_expiracion DATETIME NOT NULL,
                activa BOOLEAN DEFAULT 1,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (item_id) REFERENCES items_biblioteca (id),
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """
        )

        # Fines table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS multas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                prestamo_id INTEGER NOT NULL,
                empleado_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                descripcion TEXT NOT NULL,
                fecha_multa DATETIME DEFAULT CURRENT_TIMESTAMP,
                pagada BOOLEAN DEFAULT 0,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (prestamo_id) REFERENCES prestamos (id),
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """
        )

        self._connection.commit()

    def __enter__(self):
        return self.get_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
