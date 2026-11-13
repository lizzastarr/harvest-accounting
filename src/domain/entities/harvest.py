"""Сутність «Запис про врожай»."""
from dataclasses import dataclass
from datetime import date
from enum import IntEnum

from src.domain.errors import DomainError


class Grade(IntEnum):
    """Сортність зібраної продукції (1 — найвищий сорт)."""

    FIRST = 1
    SECOND = 2
    THIRD = 3


@dataclass
class Harvest:
    id: str
    crop: str
    field: str
    harvest_date: date
    weight_kg: float
    grade: Grade = Grade.FIRST
    note: str = ""

    def __post_init__(self) -> None:
        if not self.crop.strip():
            raise DomainError("Назва культури не може бути порожньою")
        if not self.field.strip():
            raise DomainError("Назва поля не може бути порожньою")
        if self.weight_kg <= 0:
            raise DomainError("Вага врожаю має бути більшою за нуль")
        if self.harvest_date > date.today():
            raise DomainError("Дата збору не може бути в майбутньому")
