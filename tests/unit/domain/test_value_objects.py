"""
Tests for domain value objects
"""

import pytest

from src.domain.value_objects import ISBN, Email, Money


class TestEmail:
    def test_valid_email_creation(self):
        email = Email("test@example.com")
        assert email.value == "test@example.com"
        assert str(email) == "test@example.com"

    def test_invalid_email_raises_exception(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("invalid-email")

        with pytest.raises(ValueError, match="Invalid email format"):
            Email("test@")

        with pytest.raises(ValueError, match="Invalid email format"):
            Email("@example.com")

    def test_email_immutability(self):
        email = Email("test@example.com")
        # Should not be able to modify value
        with pytest.raises(AttributeError):
            email.value = "other@example.com"


class TestMoney:
    def test_valid_money_creation(self):
        money = Money(100.50)
        assert money.amount == 100.50
        assert money.currency == "ARS"
        assert str(money) == "ARS 100.50"

    def test_money_with_custom_currency(self):
        money = Money(50.0, "USD")
        assert money.currency == "USD"
        assert str(money) == "USD 50.00"

    def test_negative_amount_raises_exception(self):
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money(-10.0)

    def test_money_addition(self):
        money1 = Money(100.0)
        money2 = Money(50.0)
        result = money1 + money2
        assert result.amount == 150.0
        assert result.currency == "ARS"

    def test_money_subtraction(self):
        money1 = Money(100.0)
        money2 = Money(30.0)
        result = money1 - money2
        assert result.amount == 70.0
        assert result.currency == "ARS"

    def test_money_operations_different_currencies_fail(self):
        money_ars = Money(100.0, "ARS")
        money_usd = Money(50.0, "USD")

        with pytest.raises(ValueError, match="Cannot add money with different currencies"):
            money_ars + money_usd

        with pytest.raises(ValueError, match="Cannot subtract money with different currencies"):
            money_ars - money_usd


class TestISBN:
    def test_valid_isbn10(self):
        isbn = ISBN("1234567890")
        assert isbn.value == "1234567890"

    def test_valid_isbn13(self):
        isbn = ISBN("1234567890123")
        assert isbn.value == "1234567890123"

    def test_valid_isbn_with_hyphens(self):
        isbn = ISBN("978-3-16-148410-0")
        assert isbn.value == "978-3-16-148410-0"

    def test_invalid_isbn_length(self):
        with pytest.raises(ValueError, match="Invalid ISBN format"):
            ISBN("123456789")  # Too short

        with pytest.raises(ValueError, match="Invalid ISBN format"):
            ISBN("12345678901234")  # Too long

    def test_invalid_isbn_characters(self):
        with pytest.raises(ValueError, match="Invalid ISBN format"):
            ISBN("123456789a")

    def test_isbn_immutability(self):
        isbn = ISBN("1234567890")
        with pytest.raises(AttributeError):
            isbn.value = "0987654321"
