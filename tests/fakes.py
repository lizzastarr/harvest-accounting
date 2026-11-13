"""Тестовий дубль репозиторію: Application тестується без Infrastructure."""
from typing import Dict, List, Optional

from src.domain.entities.harvest import Harvest
from src.domain.interfaces.harvest_repository import IHarvestRepository


class FakeRepository(IHarvestRepository):
    def __init__(self) -> None:
        self.items: Dict[str, Harvest] = {}

    def add(self, harvest: Harvest) -> None:
        self.items[harvest.id] = harvest

    def get(self, harvest_id: str) -> Optional[Harvest]:
        return self.items.get(harvest_id)

    def list_all(self) -> List[Harvest]:
        return list(self.items.values())

    def delete(self, harvest_id: str) -> bool:
        return self.items.pop(harvest_id, None) is not None
