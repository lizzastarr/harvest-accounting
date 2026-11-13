"""Сховище в оперативній пам'яті (для тестів і демо)."""
from typing import Dict, List, Optional

from src.domain.entities.harvest import Harvest
from src.domain.interfaces.harvest_repository import IHarvestRepository


class InMemoryHarvestRepository(IHarvestRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Harvest] = {}

    def add(self, harvest: Harvest) -> None:
        self._items[harvest.id] = harvest

    def get(self, harvest_id: str) -> Optional[Harvest]:
        return self._items.get(harvest_id)

    def list_all(self) -> List[Harvest]:
        return list(self._items.values())

    def delete(self, harvest_id: str) -> bool:
        return self._items.pop(harvest_id, None) is not None
