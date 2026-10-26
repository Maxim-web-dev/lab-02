import pytest

from streamstats.errors import WrongEvent, WrongFormat, WrongTimeFormat
from streamstats.parsers import parse_event


def test_parsers_1 ():
	assert parse_event({'timestamp': '2026-10-07T08:00:00', 'level': 'WARNING', 'source': 'api', 'message': 'slow'}) == {'timestamp': '2026-10-07T08:00:00', 'level': 'WARNING', 'source': 'api', 'message': 'slow'}

def test_parsers_2 ():
	assert parse_event({'timestamp': '2026-10-06T10:00:00', 'level': 'INFO', 'source': 'api', 'message': 'start'}) == {'timestamp': '2026-10-06T10:00:00', 'level': 'INFO', 'source': 'api', 'message': 'start'}

def test_parsers_21 ():
	assert parse_event({'timestamp': '2026-10-06T10:00:00', 'level': 'INFO', 'source': 'api', 'message': ''}) == {'timestamp': '2026-10-06T10:00:00', 'level': 'INFO', 'source': 'api', 'message': ''}

def test_parsers_3 ():
	with pytest.raises(WrongTimeFormat):
		parse_event({"timestamp": "2026-10-6T10:01:00", "level": "INFO", "source": "api", "message": "всё ок"})

def test_parsers_4 ():
	with pytest.raises(WrongFormat):
		parse_event({"timestamp": "2026-10-06T10:01:00","source": "api", "level": "info", "message": "всё ок"})

def test_parsers_5 ():
	with pytest.raises(WrongEvent):
		parse_event({"timestamp": "2026-10-06T10:01:00","source": "api", "level": "INFO"})

def test_parsers_6 ():
	with pytest.raises(WrongFormat):
		parse_event({"timestamp": "2026-10-06T10:01:00", "level": "INFO", "source": " ", "message": "всё ок"})

