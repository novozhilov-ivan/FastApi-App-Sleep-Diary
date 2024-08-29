from dataclasses import dataclass, field
from typing import Any
from typing_extensions import Self

from flask import RequestBase


@dataclass
class DictPayload(RequestBase):
    json_with_any: Any
    payload: dict = field(
        default_factory=lambda: {},
        init=False,
    )

    def __post_init__(self: Self) -> None:
        if isinstance(self._json_with_any, dict):
            self.payload = self._json_with_any
