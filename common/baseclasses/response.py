from typing import Type

from werkzeug.test import TestResponse
from pydantic import BaseModel, ValidationError


class Response:
    def __init__(self, response: TestResponse):
        self.response: TestResponse = response
        self.response_json: dict | list[dict] = response.json
        self.response_status: int | list[int] = response.status_code

    def validate(self, schema: Type[BaseModel] | ValidationError) -> None:
        if issubclass(schema, BaseModel):
            self._validate(schema)
        elif issubclass(schema, Exception):
            assert issubclass(schema, ValidationError)
        else:
            assert schema is False, 'unknown schema'

    def _validate(self, schema: Type[BaseModel]) -> None:
        if isinstance(self.response_json, list):
            for item in self.response_json:
                schema.model_validate(item)
        else:
            schema.model_validate(self.response_json)

    def assert_status_code(self, status_code: int | list[int]):
        if isinstance(status_code, list):
            assert self.response_status in status_code, self
        else:
            assert self.response_status == status_code, self
        return self

    def assert_data(self, expectation):
        assert self.response_json == expectation, self
        return self

    def __str__(self):
        error_message = (
            f"\nStatus code: {self.response_status}\n"
            f"Requested url: {self.response.request.full_path}\n"
            f"Response body: {self.response_json}\n"
        )
        return error_message
