import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DatabaseConfig:
    path: str = "data/biblioteca.db"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(path=os.getenv("DB_PATH", cls.path))


@dataclass
class BibliotecaConfig:
    dias_prestamo_default: int = 15
    dias_reserva_default: int = 3
    multa_por_dia_atraso: float = 50.0
    max_prestamos_simultaneos: int = 3
    max_reservas_simultaneas: int = 2

    @classmethod
    def from_env(cls) -> "BibliotecaConfig":
        return cls(
            dias_prestamo_default=int(os.getenv("DIAS_PRESTAMO_DEFAULT", cls.dias_prestamo_default)),
            dias_reserva_default=int(os.getenv("DIAS_RESERVA_DEFAULT", cls.dias_reserva_default)),
            multa_por_dia_atraso=float(os.getenv("MULTA_POR_DIA_ATRASO", cls.multa_por_dia_atraso)),
            max_prestamos_simultaneos=int(os.getenv("MAX_PRESTAMOS_SIMULTANEOS", cls.max_prestamos_simultaneos)),
            max_reservas_simultaneas=int(os.getenv("MAX_RESERVAS_SIMULTANEAS", cls.max_reservas_simultaneas)),
        )


@dataclass
class AppConfig:
    database: DatabaseConfig
    biblioteca: BibliotecaConfig
    debug: bool = False

    @classmethod
    def load(cls) -> "AppConfig":
        return cls(
            database=DatabaseConfig.from_env(),
            biblioteca=BibliotecaConfig.from_env(),
            debug=os.getenv("DEBUG", "False").lower() == "true",
        )


def get_config() -> AppConfig:
    return AppConfig.load()
