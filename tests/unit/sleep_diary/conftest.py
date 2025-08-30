from dataclasses import dataclass

from src.domain.sleep_diary.values.points import Points


@dataclass(frozen=True)
class FakePoints(Points):
    def validate(self) -> None:
        pass
