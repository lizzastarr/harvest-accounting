"""Помилки доменного шару."""


class DomainError(Exception):
    """Порушення бізнес-правила."""


class HarvestNotFoundError(DomainError):
    """Запис про врожай не знайдено."""
