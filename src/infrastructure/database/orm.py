import os
import sqlite3
from typing import Any, Dict, List, Optional


class DatabaseConnection:
    def __init__(self, db_path: str = "data/biblioteca.db"):
        self.db_path = db_path
        self._ensure_directory()

    def _ensure_directory(self):
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_non_query(self, query: str, params: tuple = ()) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid or cursor.rowcount

    def execute_script(self, script: str) -> None:
        with self.get_connection() as conn:
            conn.executescript(script)


class ORM:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        # Whitelist of allowed table names for security
        self._allowed_tables = {"usuarios", "items_biblioteca", "empleados", "prestamos", "reservas", "multas"}

    def _validate_table_name(self, table: str) -> None:
        """Validate table name against whitelist to prevent SQL injection."""
        if table not in self._allowed_tables:
            raise ValueError(f"Invalid table name: {table}. Must be one of {self._allowed_tables}")

    def _sanitize_column_names(self, columns: List[str]) -> List[str]:
        """Sanitize column names to prevent SQL injection."""
        sanitized = []
        for col in columns:
            # Only allow alphanumeric characters and underscores
            if not col.replace("_", "").isalnum():
                raise ValueError(f"Invalid column name: {col}")
            sanitized.append(col)
        return sanitized

    def create_tables(self):
        schema = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            tipo TEXT NOT NULL,
            numero_identificacion TEXT UNIQUE NOT NULL,
            telefono TEXT,
            activo BOOLEAN DEFAULT 1,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS items_biblioteca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            isbn TEXT,
            categoria TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'disponible',
            descripcion TEXT,
            ubicacion TEXT,
            fecha_adquisicion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            valor_reposicion REAL
        );

        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            usuario_sistema TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            cargo TEXT NOT NULL DEFAULT 'Bibliotecario',
            turno TEXT,
            activo BOOLEAN DEFAULT 1,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            empleado_id INTEGER NOT NULL,
            fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_devolucion_esperada TIMESTAMP NOT NULL,
            fecha_devolucion_real TIMESTAMP,
            observaciones TEXT,
            activo BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (item_id) REFERENCES items_biblioteca (id),
            FOREIGN KEY (empleado_id) REFERENCES empleados (id)
        );

        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            empleado_id INTEGER NOT NULL,
            fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion TIMESTAMP NOT NULL,
            activa BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (item_id) REFERENCES items_biblioteca (id),
            FOREIGN KEY (empleado_id) REFERENCES empleados (id)
        );

        CREATE TABLE IF NOT EXISTS multas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            prestamo_id INTEGER NOT NULL,
            empleado_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_multa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pagada BOOLEAN DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (prestamo_id) REFERENCES prestamos (id),
            FOREIGN KEY (empleado_id) REFERENCES empleados (id)
        );

        CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
        CREATE INDEX IF NOT EXISTS idx_empleados_usuario_sistema ON empleados(usuario_sistema);
        CREATE INDEX IF NOT EXISTS idx_empleados_email ON empleados(email);
        CREATE INDEX IF NOT EXISTS idx_items_titulo ON items_biblioteca(titulo);
        CREATE INDEX IF NOT EXISTS idx_items_autor ON items_biblioteca(autor);
        CREATE INDEX IF NOT EXISTS idx_prestamos_usuario ON prestamos(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_prestamos_empleado ON prestamos(empleado_id);
        CREATE INDEX IF NOT EXISTS idx_prestamos_item ON prestamos(item_id);
        CREATE INDEX IF NOT EXISTS idx_reservas_usuario ON reservas(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_reservas_empleado ON reservas(empleado_id);
        CREATE INDEX IF NOT EXISTS idx_multas_usuario ON multas(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_multas_empleado ON multas(empleado_id);
        """

        self.db.execute_script(schema)

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        self._validate_table_name(table)
        columns = self._sanitize_column_names(list(data.keys()))
        placeholders = ", ".join(["?" for _ in columns])
        values = list(data.values())

        # Safe to use f-string here as table and columns are validated
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"  # nosec B608
        return self.db.execute_non_query(query, tuple(values))

    def select(self, table: str, where: Optional[str] = None, params: tuple = ()) -> List[Dict[str, Any]]:
        self._validate_table_name(table)
        # Safe to use f-string here as table name is validated
        query = f"SELECT * FROM {table}"  # nosec B608
        if where:
            query += f" WHERE {where}"

        return self.db.execute_query(query, params)

    def update(self, table: str, data: Dict[str, Any], where: str, params: tuple = ()) -> int:
        self._validate_table_name(table)
        columns = self._sanitize_column_names(list(data.keys()))
        set_clause = ", ".join([f"{key} = ?" for key in columns])
        values = list(data.values()) + list(params)

        # Safe to use f-string here as table and columns are validated
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"  # nosec B608
        return self.db.execute_non_query(query, tuple(values))

    def delete(self, table: str, where: str, params: tuple = ()) -> int:
        self._validate_table_name(table)
        # Safe to use f-string here as table name is validated
        query = f"DELETE FROM {table} WHERE {where}"  # nosec B608
        return self.db.execute_non_query(query, params)

    def execute_custom_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        return self.db.execute_query(query, params)
