from typing import Type

from flask_restx import Namespace
from flask_restx.reqparse import RequestParser
from pydantic import BaseModel


def create_payload(
        location: str,
        ns: Namespace,
        model: Type[BaseModel]
) -> RequestParser:
    if location not in ('json', 'args'):
        raise ValueError

    payload = ns.parser()
    for field_key, field_value in model.model_fields.items():
        payload.add_argument(
            name=field_value.alias,
            type=field_value.annotation,
            required=field_value.is_required(),
            help=field_value.description,
            location=location,
        )
    return payload
