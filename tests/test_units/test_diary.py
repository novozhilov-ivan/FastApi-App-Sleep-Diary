import pytest

from src.domain.note.model import Note


def make_diary_and_note() -> tuple[Note, "Diary"]: ...


@pytest.mark.xfail(reason="todo")
def test_write_note(): ...


@pytest.mark.xfail(reason="todo")
def test_erase_note(): ...


@pytest.mark.xfail(reason="todo")
def test_cannot_twice_write_note(): ...


@pytest.mark.xfail(reason="todo")
def test_can_only_erase_written_note(): ...


@pytest.mark.xfail(reason="todo")
def test_can_only_erase_written_note(): ...
