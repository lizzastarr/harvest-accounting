import unittest
from datetime import date

from src.application.use_cases.add_harvest import AddHarvestUseCase
from src.application.use_cases.delete_harvest import DeleteHarvestUseCase
from src.application.use_cases.harvest_report import HarvestReportUseCase
from src.application.use_cases.list_harvests import ListHarvestsUseCase
from src.domain.errors import HarvestNotFoundError
from tests.fakes import FakeRepository


class UseCaseTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRepository()
        self.add = AddHarvestUseCase(self.repo)
        self.d = date(2026, 8, 1)

    def test_add_and_list_filter(self):
        self.add.execute("пшениця", "Поле 1", self.d, 1000)
        self.add.execute("кукурудза", "Поле 2", self.d, 2000)
        lst = ListHarvestsUseCase(self.repo)
        self.assertEqual(len(lst.execute()), 2)
        self.assertEqual(len(lst.execute(crop="Пшениця")), 1)
        self.assertEqual(len(lst.execute(field="Поле 2")), 1)

    def test_delete(self):
        h = self.add.execute("Пшениця", "Поле 1", self.d, 1000)
        DeleteHarvestUseCase(self.repo).execute(h.id)
        self.assertEqual(self.repo.list_all(), [])
        with self.assertRaises(HarvestNotFoundError):
            DeleteHarvestUseCase(self.repo).execute(h.id)

    def test_report_totals_sorted(self):
        self.add.execute("Пшениця", "Поле 1", self.d, 1000)
        self.add.execute("Пшениця", "Поле 2", self.d, 500)
        self.add.execute("Кукурудза", "Поле 3", self.d, 3000)
        rep = HarvestReportUseCase(self.repo).execute()
        self.assertEqual([r.crop for r in rep], ["Кукурудза", "Пшениця"])
        self.assertEqual(rep[1].total_kg, 1500)
        self.assertEqual(rep[1].records, 2)


if __name__ == "__main__":
    unittest.main()
