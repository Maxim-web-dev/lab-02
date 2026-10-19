def update_stats(event: dict, stats: dict) -> dict:
    """Получаем на вход словари: новое событие и текущую статистику. Обновляем статистику и возвращаем ее"""
    stats["total"] += 1

    ts = event["timestamp"]
    stats["first_timestamp"] = (
        min(stats["first_timestamp"], ts) if stats["first_timestamp"] else ts
    )

    stats["last_timestamp"] = max(stats["last_timestamp"], ts)
    stats["by_level"][event["level"]] += 1

    src = event["source"]
    stats["by_source"][src] = stats["by_source"].get(src, 0) + 1

    if event["level"] in ("ERROR", "CRITICAL"):
        stats["top_error_sources"][src] = stats["top_error_sources"].get(src, 0) + 1

    return stats
