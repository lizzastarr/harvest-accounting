"""Use case: переглянути записи про врожай."""
from typing import List, Optional

from src.domain.entities.harvest import Harvest
from src.domain.interfaces.harvest_repository import IHarvestRepository


class ListHarvestsUseCase:
    def __init__(self, repository: IHarvestRepository) -> None:
        self._repository = repository

    def execute(self, crop: Optional[str] = None,
                field: Optional[str] = None) -> List[Harvest]:
        items = self._repository.list_all()
        if crop:
            items = [h for h in items if h.crop == crop.strip().capitalize()]
        if field:
            items = [h for h in items if h.field == field.strip()]
        return sorted(items, key=lambda h: h.harvest_date)
