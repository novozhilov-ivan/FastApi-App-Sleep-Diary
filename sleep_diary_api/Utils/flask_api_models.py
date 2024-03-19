from copy import deepcopy
from typing import Type

import jsonref
from flask_restx import Namespace
from pydantic import BaseModel


def flask_restx_schema(ns: Namespace, pydantic_model: Type[BaseModel]):
    schema = pydantic_model.model_json_schema(by_alias=True)
    schema = str(schema)
    schema = schema.replace("'", '"')
    schema = schema.replace("None", "null")
    json_schema = deepcopy(jsonref.loads(schema))
    return ns.schema_model(pydantic_model.__name__, json_schema)
