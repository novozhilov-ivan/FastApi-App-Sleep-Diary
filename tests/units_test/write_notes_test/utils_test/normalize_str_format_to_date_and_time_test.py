import datetime as dt

from src.domain import note as nt


def test_normalize_str_to_date() -> None:
    assert nt.normalize_str_to_date("2020-12-12") == dt.date(2020, 12, 12)


def test_normalize_str_to_time() -> None:
    assert nt.normalize_str_to_time("12:50") == dt.time(12, 50)
