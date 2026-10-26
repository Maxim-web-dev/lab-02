# Потоковый анализатор файлов

Пакет `streamstats`, читающий события из CSV и JSONL построчно, без полной загрузки в память, и создающий статистический отчёт. Работает через консоль CLI.

## Возможности
- Потоковое чтение файлов, память не зависит от размера файлов.
- Режим `--skip-invalid` пропускает неверные строки и логирует `WARNING`, записывая количество пропущенных строк в отчет.
- При ошибке выводится путь файла и номер строки.
- Вывод общего количества событий, разных уровней, из разных источников и топ 5 источников событий уровня ERROR и CRITICAL.
- Вывод первой и последней временной метки (Timestamp).
- Вывод отчета в консоль или в отдельный файл в формате JSON.
- Объединение статистики нескольких файлов в один отчет.

## Установка
```bash
git clone https://github.com/Maxim-web-dev/lab-02.git
cd lab-02
pip install -e .
```

## Использование
```bash
python -m streamstats analyze INPUT [INPUT ...] --format "csv|jsonl" --output REPORT.json
python -m streamstats analyze data/events.csv --format csv --output report.json
python -m streamstats analyze b.jsonl --format jsonl --skip-invalid
python -m streamstats analyze a.csv b.jsonl --format "csv|jsonl"
python -m streamstats --help
```

На macOS при использовании может понадобиться запись `python3`, вместо `python`.

- `INPUT` - один или несколько файлов через пробел.
- `--format` - `csv`, `jsonl` формат входного файла или `"csv|jsonl"`, если форматы файлов разные.
- `--output` - необязательный флаг: куда записать JSON-отчёт; если не указан, отчёт выводится в консоль.
- `--skip-invalid` - необязательный флаг: пропускать ли некорректные строки (`WARNING` в `stderr`), иначе остановка с кодом 2

## Примеры входных данных

Пример CSV (`events.csv`):

```csv
timestamp,level,source,message
2026-10-06T10:00:00,INFO,api,start
2026-10-06T11:00:00,ERROR,db,fail
2026-10-06T11:00:00,WARNING,db,restart
```

Пример JSONL (`events.jsonl`):

```json
{"timestamp": "2026-10-07T08:00:00", "level": "WARNING", "source": "api", "message": "slow"}
{"timestamp": "2026-10-07T09:00:00", "level": "ERROR", "source": "api", "message": "500"}
{"timestamp": "2026-10-05T07:00:00", "level": "INFO", "source": "worker", "message": "done"}
```

## Пример отчёта
```json
{
    "first_timestamp": "2026-10-06T00:00:00",
    "last_timestamp": "2026-12-06T12:00:00",
    "total": 9,
    "by_level": {
        "DEBUG": 1,
        "INFO": 6,
        "WARNING": 1,
        "ERROR": 1,
        "CRITICAL": 0
    },
    "by_source": {
        "api": 7,
        "db": 2
    },
    "top_error_sources": {
        "db": 1
    },
    "skipped_rows": 1
}
```

## Ошибки
- При ошибке c `--skip-invalid` `Warning` в лог с указанием ошибочной строки и файла. Завершение с кодом 0 и выводом количества пропущенных строк.
- Без `--skip-invalid` сообщение с ошибкой в stderr и код 2. 
- При успехе — код 0.

## Тесты
```bash
python -m pytest
python -m ruff check .
```