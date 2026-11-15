"""Консольний інтерфейс: python -m src.presentation.cli <команда>."""
import argparse
import logging
import sys
from datetime import date

from src.domain.entities.harvest import Grade
from src.domain.errors import DomainError
from src.infrastructure.settings import load_settings
from src.presentation.composition import build_container


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harvest", description="Облік урожаю")
    p.add_argument("--config", default="appsettings.json")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="додати запис про врожай")
    a.add_argument("--crop", required=True, help="культура")
    a.add_argument("--field", required=True, help="поле")
    a.add_argument("--weight", type=float, required=True, help="вага, кг")
    a.add_argument("--date", type=date.fromisoformat, default=date.today(),
                   help="дата збору РРРР-ММ-ДД")
    a.add_argument("--grade", type=int, choices=[1, 2, 3], default=1)
    a.add_argument("--note", default="")

    l = sub.add_parser("list", help="показати записи")
    l.add_argument("--crop")
    l.add_argument("--field")

    d = sub.add_parser("delete", help="видалити запис за id")
    d.add_argument("id")

    sub.add_parser("report", help="підсумок по культурах")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(args.config)
    logging.basicConfig(level=settings.log_level)
    app = build_container(settings)
    try:
        if args.command == "add":
            h = app.add.execute(args.crop, args.field, args.date, args.weight,
                                Grade(args.grade), args.note)
            print(f"Додано запис {h.id}: {h.crop}, {h.weight_kg:g} кг")
        elif args.command == "list":
            items = app.list.execute(args.crop, args.field)
            if not items:
                print("Записів немає")
            for h in items:
                print(f"{h.id}  {h.harvest_date}  {h.crop:<12} {h.field:<10} "
                      f"{h.weight_kg:>10.1f} кг  сорт {int(h.grade)}  {h.note}")
        elif args.command == "delete":
            app.delete.execute(args.id)
            print(f"Запис {args.id} видалено")
        elif args.command == "report":
            rows = app.report.execute()
            if not rows:
                print("Записів немає")
            for r in rows:
                print(f"{r.crop:<12} записів: {r.records:<3} разом: {r.total_kg:>10.1f} кг")
            if rows:
                print(f"{'РАЗОМ':<12} {'':<13} {sum(r.total_kg for r in rows):>10.1f} кг")
    except DomainError as e:
        print(f"Помилка: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
