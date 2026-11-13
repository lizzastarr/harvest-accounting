"""Сутність «Запис про врожай»."""
from dataclasses import dataclass
from datetime import date
from enum import IntEnum


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
