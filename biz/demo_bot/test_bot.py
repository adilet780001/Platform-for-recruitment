import tempfile
from pathlib import Path
import bot

def test_phone():
    assert bot.normalize_phone("+7 (701) 123-45-67") == "+77011234567"
    assert bot.normalize_phone("87011234567") == "87011234567"
    assert bot.normalize_phone("12345") is None

def test_save_booking():
    p = Path(tempfile.mkdtemp()) / "b.csv"
    bot.save_booking({"a": 1, "b": 2}, p); bot.save_booking({"a": 3, "b": 4}, p)
    assert p.read_text().splitlines() == ["a,b", "1,2", "3,4"]

def test_app_builds():
    assert bot.build_app("123:ABC").handlers
