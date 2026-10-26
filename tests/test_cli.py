import json
import subprocess
import sys


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "streamstats", *args],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )


def test_valid_csv():
    result = run_cli("analyze", "tests/data/test_valid.csv", "--format", "csv")
    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "first_timestamp": "2026-10-06T09:00:00",
        "last_timestamp": "2026-10-06T13:00:00",
        "total": 5,
        "by_level": {"DEBUG": 1, "INFO": 1, "WARNING": 0, "ERROR": 2, "CRITICAL": 1},
        "by_source": {"api": 2, "db": 2, "web": 1},
        "top_error_sources": {"db": 2, "api": 1},
        "skipped_rows": 0,
    }


def test_valid_jsonl():
    result = run_cli("analyze", "tests/data/test_valid.jsonl", "--format", "jsonl")
    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "first_timestamp": "2026-10-05T07:00:00",
        "last_timestamp": "2026-10-07T09:00:00",
        "total": 3,
        "by_level": {"DEBUG": 0, "INFO": 1, "WARNING": 1, "ERROR": 1, "CRITICAL": 0},
        "by_source": {"api": 2, "worker": 1},
        "top_error_sources": {"api": 1},
        "skipped_rows": 0,
    }


def test_mixed_formats():
    result = run_cli(
        "analyze",
        "tests/data/test_valid.csv",
        "tests/data/test_valid.jsonl",
        "--format",
        "csv|jsonl",
    )
    report = json.loads(result.stdout)
    assert result.returncode == 0
    assert report["total"] == 8
    assert report["by_source"] == {"api": 4, "db": 2, "web": 1, "worker": 1}
    assert report["top_error_sources"] == {"db": 2, "api": 2}
    assert report["first_timestamp"] == "2026-10-05T07:00:00"
    assert report["last_timestamp"] == "2026-10-07T09:00:00"


def test_empty_csv():
    result = run_cli("analyze", "tests/data/empty.csv", "--format", "csv")
    report = json.loads(result.stdout)
    assert result.returncode == 0
    assert report["total"] == 0
    assert report["first_timestamp"] == ""


def test_empty_jsonl():
    result = run_cli("analyze", "tests/data/empty.jsonl", "--format", "jsonl")
    assert result.returncode == 0
    assert json.loads(result.stdout)["total"] == 0


def test_bad_jsonl_default_mode():
    result = run_cli("analyze", "tests/data/bad.jsonl", "--format", "jsonl")
    assert result.returncode == 2
    assert "№2" in result.stderr
    assert "bad.jsonl" in result.stderr
    assert result.stdout == ""


def test_bad_jsonl_skip_invalid():
    result = run_cli(
        "analyze", "tests/data/bad.jsonl", "--format", "jsonl", "--skip-invalid"
    )
    report = json.loads(result.stdout)
    assert result.returncode == 0
    assert report["total"] == 2
    assert report["skipped_rows"] == 4
    assert report["last_timestamp"] == "2026-10-06T10:05:00"
    assert result.stderr.count("WARNING") == 4


def test_bad_csv_default_mode():
    result = run_cli("analyze", "tests/data/bad.csv", "--format", "csv")
    assert result.returncode == 2
    assert "№3" in result.stderr
    assert result.stdout == ""


def test_bad_csv_skip_invalid():
    result = run_cli(
        "analyze", "tests/data/bad.csv", "--format", "csv", "--skip-invalid"
    )
    report = json.loads(result.stdout)
    assert result.returncode == 0
    assert report["total"] == 2
    assert report["skipped_rows"] == 1
    assert report["top_error_sources"] == {"db": 1}


def test_unicode():
    result = run_cli("analyze", "tests/data/unicode.jsonl", "--format", "jsonl")
    assert result.returncode == 0
    assert "сервис-платежей" in result.stdout
    assert json.loads(result.stdout)["top_error_sources"] == {"сервис-платежей": 1}


def test_invalid_format():
    result = run_cli("analyze", "tests/data/test_valid.csv", "--format", "xml")
    assert result.returncode == 2


def test_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "analyze" in result.stdout
