from typing import Literal, Type

from flask_restx.reqparse import RequestParser
from pydantic import BaseModel


#  TODO Переделать на создание словаря, как в /note/
def create_payload_from_model(
    location: Literal["json", "args", "files", "form"],
    model: Type[BaseModel],
) -> RequestParser:
    payload = RequestParser()
    for field, field_info in model.model_fields.items():
        create_payload(
            name=field,
            type_=field_info.annotation,
            required=field_info.is_required(),
            description=field_info.description,
            location=location,
            payload=payload,
        )
    return payload


def create_payload(
    name: str,
    type_: Type[str] | None,
    description: str,
    location: Literal["json", "args", "files", "form", "headers"],
    required: bool = True,
    payload: RequestParser | None = None,
) -> RequestParser:

    if payload is None:
        payload = RequestParser()
    payload.add_argument(
        name=name,
        type=type_,
        required=required,
        help=description,
        location=location,
    )
    return payload
