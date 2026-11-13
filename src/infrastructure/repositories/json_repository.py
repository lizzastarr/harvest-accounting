"""Сховище у JSON-файлі."""
import json
import os
from datetime import date
from typing import Dict, List, Optional

from src.domain.entities.harvest import Grade, Harvest
from src.domain.interfaces.harvest_repository import IHarvestRepository


class JsonHarvestRepository(IHarvestRepository):
    def __init__(self, path: str) -> None:
        self._path = path

    # --- серіалізація ---
    @staticmethod
    def _to_dict(h: Harvest) -> dict:
        return {"id": h.id, "crop": h.crop, "field": h.field,
                "harvest_date": h.harvest_date.isoformat(),
                "weight_kg": h.weight_kg, "grade": int(h.grade), "note": h.note}

    @staticmethod
    def _from_dict(d: dict) -> Harvest:
        return Harvest(d["id"], d["crop"], d["field"],
                       date.fromisoformat(d["harvest_date"]),
                       d["weight_kg"], Grade(d["grade"]), d.get("note", ""))

    def _load(self) -> Dict[str, Harvest]:
        if not os.path.exists(self._path):
            return {}
        with open(self._path, encoding="utf-8") as f:
            return {d["id"]: self._from_dict(d) for d in json.load(f)}

    def _save(self, items: Dict[str, Harvest]) -> None:
        folder = os.path.dirname(self._path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([self._to_dict(h) for h in items.values()], f,
                      ensure_ascii=False, indent=2)

    # --- IHarvestRepository ---
    def add(self, harvest: Harvest) -> None:
        items = self._load()
        items[harvest.id] = harvest
        self._save(items)

    def get(self, harvest_id: str) -> Optional[Harvest]:
        return self._load().get(harvest_id)

    def list_all(self) -> List[Harvest]:
        return list(self._load().values())

    def delete(self, harvest_id: str) -> bool:
        items = self._load()
        if items.pop(harvest_id, None) is None:
            return False
        self._save(items)
        return True
