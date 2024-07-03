from src.domain import note


class NoteValueObject(
    note.TimePointsSequencesValidator,
    note.NoSleepDurationValidator,
    note.NoteDurations,
    note.NoteStatistic,
    note.NoteBase,
):
    ...  # fmt: skip
