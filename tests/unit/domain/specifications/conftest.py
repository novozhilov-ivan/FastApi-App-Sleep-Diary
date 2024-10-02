from typing_extensions import Self

from src.domain.values.points import Points


class FakePoints(Points):
    def validate(self: Self) -> None: ...
