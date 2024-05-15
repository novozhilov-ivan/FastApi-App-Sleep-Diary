from datetime import date

from flask_restx import Resource

from api.routes import ns_sleep
from api.routes.sleep.note_read import response_model_200
from common.baseclasses.status_codes import HTTP


@ns_sleep.response(**response_model_200)
class NoteReadRoute(Resource):
    """Чтение записи из дневника сна"""

    @ns_sleep.doc(description=__doc__)
    def get(self, calendar_date: date):
        return {"calendar_date": calendar_date}, HTTP.OK_200
