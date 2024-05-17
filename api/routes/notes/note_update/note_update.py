from api.routes.notes import ns_notes
from api.routes.notes.note_update import response_model_204


class UpdateNote:
    @ns_notes.response(**response_model_204)
    def patch(self):
        pass
