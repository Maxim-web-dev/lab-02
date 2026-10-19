from datetime import datetime

from streamstats.errors import WrongEvent, WrongFormat, WrongTimeFormat

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
REQUIRED_KEYS = ("timestamp", "level", "source", "message")


def parse_event(row: dict) -> dict:
    """На вход получаем словарь. Проверяем на ошибки и верный формат. Если все хорошо - возвращаем этот же словарь, но дата в формате datetime. В противном случае вызываем ошибку."""

    missing_keys = [key for key in REQUIRED_KEYS if key not in row]

    if missing_keys:
        raise WrongEvent(f"Нет ключей: {', '.join(missing_keys)}")

    if not all(isinstance(row[key], str) for key in REQUIRED_KEYS):
        raise WrongFormat("все ключи должны быть строками")

    if row["level"] not in LEVELS:
        raise WrongFormat(f"level: {row['level']!r}")

    if not row["source"].strip():
        raise WrongFormat(f"source: {row['source']!r}")

    try:
        datetime.fromisoformat(row["timestamp"])
    except ValueError as exc:
        raise WrongTimeFormat(f"{row['timestamp']!r}") from exc

    return {
        "timestamp": row["timestamp"],
        "level": row["level"],
        "source": row["source"],
        "message": row["message"],
    }
