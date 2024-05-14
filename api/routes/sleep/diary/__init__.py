from api.routes import ns_sleep
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_sleep,
    model=SleepDiaryModel,
)
response_model_404 = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_sleep,
    model=SleepDiaryModelEmpty,
)

from api.routes.sleep.diary.diary import DiaryRoute  # noqa

diary_endpoint = "diary"
ns_sleep.add_resource(
    DiaryRoute,
    f"/{diary_endpoint}",
    endpoint=diary_endpoint,
)
