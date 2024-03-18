from copy import deepcopy
from typing import Type

import jsonref
from flask_restx import Namespace
from pydantic import BaseModel


def flask_restx_schema(ns: Namespace, pydantic_model: Type[BaseModel]):
    json_schema = deepcopy(jsonref.loads(pydantic_model.schema_json()))
    return ns.schema_model(pydantic_model.__name__, json_schema)
