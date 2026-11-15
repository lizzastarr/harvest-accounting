"""Use case: зареєструвати новий врожай."""
import uuid
from datetime import date

from src.domain.entities.harvest import Grade, Harvest
from src.domain.interfaces.harvest_repository import IHarvestRepository


class AddHarvestUseCase:
    def __init__(self, repository: IHarvestRepository) -> None:
        self._repository = repository

    def execute(self, crop: str, field: str, harvest_date: date,
                weight_kg: float, grade: Grade = Grade.FIRST,
                note: str = "") -> Harvest:
        harvest = Harvest(uuid.uuid4().hex[:8], crop, field, harvest_date,
                          weight_kg, grade, note)
        self._repository.add(harvest)
        return harvest
