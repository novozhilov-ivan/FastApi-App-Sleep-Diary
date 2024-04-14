from typing import Type, Generator

from werkzeug.test import TestResponse
from pydantic import BaseModel


class Response:
    def __init__(self, response: TestResponse):
        self.response: TestResponse = response
        self.response_json: dict | list[dict] | Generator[dict] = response.json
        self.response_str: str = response.get_data(as_text=True)
        self.response_status: int | list[int] = response.status_code

    def validate(self, schema: Type[BaseModel]) -> None:
        if self.response.mimetype == 'application/json':
            self.validate_json(schema)
        elif self.response.mimetype == 'text/csv':
            self.validate_str_csv(schema)

    def validate_str_csv(self, schema: Type[BaseModel]):
        rows_delimiter: str = "\n"
        columns_delimiter: str = ","
        titles, data = self.response_str.split(rows_delimiter, maxsplit=1)
        fields_title = (field.title for field in schema.model_fields.values())
        assert list(fields_title) == titles.split(columns_delimiter)
        rows = (data.split(columns_delimiter) for data in data.split(rows_delimiter) if data)
        fields = [field for field in schema.model_fields]
        self.response_json = (dict(zip(fields, row)) for row in rows)
        self.validate_json(schema)

    def validate_json(self, schema: Type[BaseModel]):
        if isinstance(self.response_json, dict):
            schema.model_validate(self.response_json)
        else:
            for item in self.response_json:
                schema.model_validate(item)

    def assert_status_code(self, status_code: int):
        assert self.response_status == status_code, self
        return self

    def assert_data(self, expectation: BaseModel | str):
        if isinstance(expectation, BaseModel):
            expectation = expectation.model_dump(mode='json')
            assert self.response_json == expectation, self
        elif isinstance(expectation, str):
            assert self.response_str == expectation, self
        return self, expectation

    def __str__(self):
        error_message = (
            f"\nStatus code: {self.response_status}\n"
            f"Requested url: {self.response.request.full_path}\n"
            f"Response body: {self.response_json}\n"
            f"Response type: {type(self.response_json)}\n"
        )
        return error_message
