from sleep_diary_api.Api_schema_models.flask_api_models import flask_restx_schema

from sleep_diary_api.Routes import ns_sleep
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryEntriesModel
from src.pydantic_schemas.notes.sleep_notes import SleepNoteMain, SleepNoteModel


# Get
sleep_get_all = flask_restx_schema(ns_sleep, SleepDiaryEntriesModel)

# Post
sleep_post_requested = flask_restx_schema(ns_sleep, SleepNoteMain)
sleep_post_created = flask_restx_schema(ns_sleep, SleepNoteModel)
