import json
from copy import deepcopy
from typing import Type

import jsonref
from flask_restx import Namespace, SchemaModel
from pydantic import BaseModel


def response_schema(
        code: int,
        description: str,
        ns: Namespace,
        model: Type[BaseModel]
) -> dict:
    return {
        "code": code,
        "description": description,
        "model": flask_restx_schema(ns, model)
    }


def flask_restx_schema(
        ns: Namespace,
        pydantic_model: Type[BaseModel]
) -> SchemaModel:
    schema = pydantic_model.model_json_schema()
    schema = json.dumps(schema)
    json_schema = deepcopy(jsonref.loads(schema))
    return ns.schema_model(pydantic_model.__name__, json_schema)
