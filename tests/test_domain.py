import unittest
from datetime import date, timedelta

from src.domain.entities.harvest import Grade, Harvest
from src.domain.errors import DomainError


class HarvestTests(unittest.TestCase):
    def make(self, **kw):
        data = dict(id="1", crop="Пшениця", field="Поле №1",
                    harvest_date=date(2026, 8, 1), weight_kg=1500.0)
        data.update(kw)
        return Harvest(**data)

    def test_valid(self):
        h = self.make()
        self.assertEqual(h.grade, Grade.FIRST)

    def test_weight_must_be_positive(self):
        with self.assertRaises(DomainError):
            self.make(weight_kg=0)

    def test_crop_required(self):
        with self.assertRaises(DomainError):
            self.make(crop="  ")

    def test_crop_is_normalized(self):
        self.assertEqual(self.make(crop="  пшениця ").crop, "Пшениця")

    def test_future_date_forbidden(self):
        with self.assertRaises(DomainError):
            self.make(harvest_date=date.today() + timedelta(days=1))


if __name__ == "__main__":
    unittest.main()
