from src.domain import note


class NoteValueObject(
    note.NoteStatistic,
    note.NoSleepDurationValidator,
    note.TimePointsSequencesValidator,
    note.NoteBase,
):
    ...  # fmt: skip
