"""Use case: видалити запис про врожай."""
from src.domain.errors import HarvestNotFoundError
from src.domain.interfaces.harvest_repository import IHarvestRepository


class DeleteHarvestUseCase:
    def __init__(self, repository: IHarvestRepository) -> None:
        self._repository = repository

    def execute(self, harvest_id: str) -> None:
        if not self._repository.delete(harvest_id):
            raise HarvestNotFoundError(f"Запис '{harvest_id}' не знайдено")
