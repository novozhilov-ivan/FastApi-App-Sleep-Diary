import pytest

from src.domain import note
from src.domain.diary.model import Diary


def make_diary_and_note() -> tuple[note.NoteValueObject, Diary]: ...


@pytest.mark.xfail(reason="todo")
def test_write_note() -> None: ...


@pytest.mark.xfail(reason="todo")
def test_cannot_twice_write_note() -> None: ...
