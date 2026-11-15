"""Абстракція сховища записів про врожай (порт)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.harvest import Harvest


class IHarvestRepository(ABC):
    @abstractmethod
    def add(self, harvest: Harvest) -> None: ...

    @abstractmethod
    def get(self, harvest_id: str) -> Optional[Harvest]: ...

    @abstractmethod
    def list_all(self) -> List[Harvest]: ...

    @abstractmethod
    def delete(self, harvest_id: str) -> bool:
        """Повертає True, якщо запис існував і був видалений."""
