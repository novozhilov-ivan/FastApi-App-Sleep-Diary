from dataclasses import dataclass
from typing_extensions import Self

from werkzeug.wrappers import Request


@dataclass
class DictFromJsonPayload(Request):
    request: Request

    @property
    def json(self: Self) -> dict:
        if isinstance(self.request.json, dict):
            return self.request.json
        return {}
