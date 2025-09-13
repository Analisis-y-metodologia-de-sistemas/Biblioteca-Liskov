"""
Value Objects for the Library Domain
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class Email:
    """Value object for email addresses"""
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Money:
    """Value object for monetary amounts"""
    amount: float
    currency: str = "ARS"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency:
            raise ValueError("Currency cannot be empty")

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.amount - other.amount, self.currency)


@dataclass(frozen=True)
class ISBN:
    """Value object for ISBN codes"""
    value: str

    def __post_init__(self):
        if not self._is_valid_isbn(self.value):
            raise ValueError(f"Invalid ISBN format: {self.value}")

    def _is_valid_isbn(self, isbn: str) -> bool:
        # Simplified ISBN validation - accepts ISBN-10 and ISBN-13
        cleaned = isbn.replace('-', '').replace(' ', '')
        return len(cleaned) in [10, 13] and cleaned.isdigit()

    def __str__(self) -> str:
        return self.value