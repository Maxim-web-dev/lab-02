import argparse
import csv
import json
import logging
import sys

from streamstats.analysis import update_stats
from streamstats.errors import StreamStatsError
from streamstats.parsers import parse_event
from streamstats.report import make_report

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

stats = {
    "first_timestamp": "",
    "last_timestamp": "",
    "total": 0,
    "by_level": {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
    "by_source": {},
    "top_error_sources": {},
    "skipped_rows": 0,
}

parser = argparse.ArgumentParser(prog="streamstats")
sub = parser.add_subparsers(dest="command", required=True)

analyze = sub.add_parser("analyze", help="Проанализировать файлы событий")
analyze.add_argument(
    "files",
    nargs="+",
    help="Файлы, которые нужно проверить. Вводится путь до каждого файла. Файлы разделяются пробелом.",
)
analyze.add_argument(
    "--format",
    choices=["csv", "jsonl", "csv|jsonl"],
    required=True,
    help="Тип вводимых файлов. Если файлы разного типа, пишется csv|jsonl.",
)
analyze.add_argument(
    "--output", help="Куда вывести результат. По умолчанию в terminal."
)
analyze.add_argument(
    "--skip-invalid",
    action="store_true",
    help="Пропускать некорректные строки вместо остановки.",
)
args = parser.parse_args()


def read_file_and_make_stats(file, path, stats):
    """Получаем на вход файл, путь к файлу и предыдущую статистику. Если файл - csv, читаем его по формату csv. Вызываем функцию parse_event. Если есть ошибки, ловим их и логируем и идем дальше (если --skip-invalid==True) или принтим и завершаем программу."""

    if args.format == "csv" or (args.format == "csv|jsonl" and path.endswith(".csv")):
        reader = csv.DictReader(file)
        rows = ((reader.line_num, row) for row in reader)
    else:
        rows = enumerate(file, 1)

    for number_of_row, row in rows:
        try:
            if isinstance(row, str):
                if not row.strip():
                    continue
                row = json.loads(row)
            event = parse_event(row)
        except (StreamStatsError, json.JSONDecodeError) as e:
            if args.skip_invalid:
                logger.warning(f"Пропущена строка №{number_of_row} в файле {path} \n")
                stats["skipped_rows"] += 1
                continue
            else:
                print(
                    f"Ошибка: {e} в файле {path} в строке №{number_of_row}",
                    file=sys.stderr,
                )
                sys.exit(2)
        except Exception as e:  # noqa: BLE001
            print(f"Неизвестная ошибка: {e}", file=sys.stderr)
            sys.exit(2)
        stats = update_stats(event, stats)
    return stats


if __name__ == "__main__":
    for path in args.files:
        with open(path, newline="", encoding="utf-8") as file:
            stats = read_file_and_make_stats(file, path, stats)
    make_report(args.output, stats)
