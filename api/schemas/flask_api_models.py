import json
from copy import deepcopy
from typing import Type

import jsonref
from flask_restx import Namespace, SchemaModel
from pydantic import BaseModel


def response_schema(
        ns: Namespace,
        code: int,
        model: Type[BaseModel],
        description: str | None = None
) -> dict:
    if description is None:
        description = model.model_json_schema().get('description')
    return {
        "code": code,
        "description": description,
        "model": flask_restx_schema(ns, model)
    }


def flask_restx_schema(
        ns: Namespace,
        model: Type[BaseModel]
) -> SchemaModel:
    schema = model.model_json_schema()
    schema = json.dumps(schema)
    json_schema = deepcopy(jsonref.loads(schema))
    return ns.schema_model(model.__name__, json_schema)
