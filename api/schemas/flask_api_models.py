import json
from copy import deepcopy
from typing import Type

import jsonref
from flask_restx import Namespace, SchemaModel
from pydantic import BaseModel


def response_schema(
    ns: Namespace,
    code: int,
    model: Type[BaseModel] | None = None,
    description: str = "No response schema description yet",
) -> dict:
    schema = {
        "code": code,
    }

    if model is not None:
        schema.update(
            {
                "description": model.model_json_schema().get("description"),
                "model": flask_restx_schema(ns, model),
            }
        )
    if schema.get("description") is None:
        schema.update(
            {
                "description": description,
            }
        )
    return schema


def flask_restx_schema(ns: Namespace, model: Type[BaseModel]) -> SchemaModel:
    schema = model.model_json_schema()
    schema = json.dumps(schema)
    json_schema = deepcopy(jsonref.loads(schema))
    return ns.schema_model(model.__name__, json_schema)
