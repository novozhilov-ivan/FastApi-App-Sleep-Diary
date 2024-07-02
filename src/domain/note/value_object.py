from src.domain import note


class NoteValueObject(
    note.NoteDurations,
    note.NoteStatistic,
    note.TimePointsSequencesValidatorBase,
    note.NoSleepDurationValidatorBase,
    note.NoteValueObjectBase,
    note.NoteDurationsBase,
):
    ...  # fmt: skip
