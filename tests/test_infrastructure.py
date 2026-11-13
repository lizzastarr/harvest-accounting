import os
import tempfile
import unittest
from datetime import date

from src.domain.entities.harvest import Grade, Harvest
from src.infrastructure.repositories.in_memory_repository import InMemoryHarvestRepository
from src.infrastructure.repositories.json_repository import JsonHarvestRepository


def sample(i="a1"):
    return Harvest(i, "Пшениця", "Поле 1", date(2026, 8, 1), 1234.5, Grade.SECOND, "тест")


class RepositoryContract:
    def make_repo(self):
        raise NotImplementedError

    def test_add_get_list_delete(self):
        repo = self.make_repo()
        repo.add(sample("a1"))
        repo.add(sample("a2"))
        self.assertEqual(repo.get("a1"), sample("a1"))
        self.assertEqual(len(repo.list_all()), 2)
        self.assertTrue(repo.delete("a1"))
        self.assertFalse(repo.delete("a1"))
        self.assertIsNone(repo.get("a1"))


class InMemoryTests(RepositoryContract, unittest.TestCase):
    def make_repo(self):
        return InMemoryHarvestRepository()


class JsonTests(RepositoryContract, unittest.TestCase):
    def make_repo(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        return JsonHarvestRepository(os.path.join(self.tmp.name, "sub", "h.json"))

    def test_persists_between_instances(self):
        repo = self.make_repo()
        repo.add(sample())
        again = JsonHarvestRepository(repo._path)
        self.assertEqual(again.list_all(), [sample()])


if __name__ == "__main__":
    unittest.main()
