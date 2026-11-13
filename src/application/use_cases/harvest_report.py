"""Use case: підсумковий звіт по культурах."""
from dataclasses import dataclass
from typing import List

from src.domain.interfaces.harvest_repository import IHarvestRepository


@dataclass(frozen=True)
class CropSummary:
    crop: str
    records: int
    total_kg: float


class HarvestReportUseCase:
    def __init__(self, repository: IHarvestRepository) -> None:
        self._repository = repository

    def execute(self) -> List[CropSummary]:
        totals: dict = {}
        for h in self._repository.list_all():
            count, kg = totals.get(h.crop, (0, 0.0))
            totals[h.crop] = (count + 1, kg + h.weight_kg)
        return sorted((CropSummary(c, n, kg) for c, (n, kg) in totals.items()),
                      key=lambda s: s.total_kg, reverse=True)
