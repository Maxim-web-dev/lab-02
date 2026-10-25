import json


def make_report (output: str | None, stats: str) -> None:
	"""Получаем на вход output (файл, в который нужно записать отчет) и статистику. Считаем топ 5 источников ошибок и выводим отчет."""
	
	stats["top_error_sources"] = dict(sorted(stats["top_error_sources"].items(), key=lambda kv: kv[1], reverse=True)[:5])
	stats = json.dumps(stats, indent=4, ensure_ascii=False)
	if output:
		with open(output, 'w', encoding='utf-8') as f:
			f.write(stats)
	else:
		print(stats)
