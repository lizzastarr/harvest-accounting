import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

from src.presentation.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = os.path.join(self.tmp.name, "cfg.json")
        self.data = os.path.join(self.tmp.name, "h.json")
        with open(self.cfg, "w", encoding="utf-8") as f:
            json.dump({"storage": {"type": "json", "path": self.data}}, f)

    def run_cli(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--config", self.cfg, *args])
        return code, out.getvalue(), err.getvalue()

    def test_full_scenario(self):
        self.assertEqual(self.run_cli("add", "--crop", "пшениця", "--field", "Поле 1",
                                      "--weight", "1500", "--date", "2026-08-01")[0], 0)
        self.run_cli("add", "--crop", "Кукурудза", "--field", "Поле 2",
                     "--weight", "3000", "--date", "2026-09-10")
        code, out, _ = self.run_cli("list")
        self.assertIn("Пшениця", out)
        code, out, _ = self.run_cli("report")
        self.assertIn("4500.0", out)
        hid = json.load(open(self.data, encoding="utf-8"))[0]["id"]
        self.assertEqual(self.run_cli("delete", hid)[0], 0)
        self.assertEqual(len(json.load(open(self.data, encoding="utf-8"))), 1)

    def test_domain_error_returns_1(self):
        code, _, err = self.run_cli("add", "--crop", "Жито", "--field", "П1", "--weight", "-5")
        self.assertEqual(code, 1)
        self.assertIn("Помилка", err)


if __name__ == "__main__":
    unittest.main()
