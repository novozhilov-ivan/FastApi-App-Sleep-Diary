from typing import Type, Literal

from flask_restx.reqparse import RequestParser
from pydantic import BaseModel


def create_payload(
        location: Literal['json', 'args'],
        model: Type[BaseModel]
) -> RequestParser:
    payload = RequestParser()
    for value in model.model_fields.values():
        payload.add_argument(
            name=value.alias,
            type=value.annotation,
            required=value.is_required(),
            help=value.description,
            location=location,
        )
    return payload
