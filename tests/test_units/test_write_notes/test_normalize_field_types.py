from datetime import date, time

from src.domain.note.utils import normalize_str_to_date, normalize_str_to_time


def test_normalize_str_to_date() -> None:
    assert normalize_str_to_date("2020-12-12") == date(2020, 12, 12)


def test_normalize_str_to_time() -> None:
    assert normalize_str_to_time("12:50") == time(12, 50)
