from typing import Type

from werkzeug.test import TestResponse
from pydantic import BaseModel


class Response:
    def __init__(self, response: TestResponse):
        self.response: TestResponse = response
        self.response_json: dict | list[dict] = response.json
        self.response_status: int | list[int] = response.status_code

    def validate(self, schema: Type[BaseModel]) -> None:
        if isinstance(self.response_json, list):
            for item in self.response_json:
                schema.model_validate(item)
        else:
            schema.model_validate(self.response_json)

    def assert_status_code(self, status_code: int):
        assert self.response_status == status_code, self
        return self

    def assert_error_data(self, errors: dict | list[dict]):
        if isinstance(errors, list):
            errors[0]['loc'] = list(errors[0]['loc'])
        self.assert_data(errors)

    def assert_data(self, expectation: BaseModel | list):
        if isinstance(expectation, BaseModel):
            expectation = expectation.model_dump(mode='json')
        assert self.response_json == expectation, self
        return self

    def __str__(self):
        error_message = (
            f"\nStatus code: {self.response_status}\n"
            f"Requested url: {self.response.request.full_path}\n"
            f"Response body: {self.response_json}\n"
            f"Response type: {type(self.response_json)}\n"
        )
        return error_message
