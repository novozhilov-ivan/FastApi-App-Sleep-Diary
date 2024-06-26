import pytest

from src.domain.diary.model import Diary
from src.domain.note.value_object import NoteValueObject


def make_diary_and_note() -> tuple[NoteValueObject, Diary]: ...


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
