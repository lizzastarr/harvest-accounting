"""Composition root: єдине місце, де створюються конкретні реалізації."""
from dataclasses import dataclass

from src.application.use_cases.add_harvest import AddHarvestUseCase
from src.application.use_cases.delete_harvest import DeleteHarvestUseCase
from src.application.use_cases.harvest_report import HarvestReportUseCase
from src.application.use_cases.list_harvests import ListHarvestsUseCase
from src.domain.interfaces.harvest_repository import IHarvestRepository
from src.infrastructure.repositories.in_memory_repository import InMemoryHarvestRepository
from src.infrastructure.repositories.json_repository import JsonHarvestRepository
from src.infrastructure.settings import Settings


@dataclass
class Container:
    add: AddHarvestUseCase
    list: ListHarvestsUseCase
    delete: DeleteHarvestUseCase
    report: HarvestReportUseCase


def create_repository(settings: Settings) -> IHarvestRepository:
    if settings.storage_type == "json":
        return JsonHarvestRepository(settings.storage_path or "data/harvests.json")
    if settings.storage_type == "memory":
        return InMemoryHarvestRepository()
    raise ValueError(f"Невідомий тип сховища: {settings.storage_type}")


def build_container(settings: Settings) -> Container:
    repository = create_repository(settings)  # Dependency Injection
    return Container(
        add=AddHarvestUseCase(repository),
        list=ListHarvestsUseCase(repository),
        delete=DeleteHarvestUseCase(repository),
        report=HarvestReportUseCase(repository),
    )
