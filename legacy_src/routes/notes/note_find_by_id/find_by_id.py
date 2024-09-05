from legacy_src.CRUD.sleep_note_table import find_user_note_by_note_id
from legacy_src.routes.account.account_find import response_model_200
from legacy_src.utils.auth import UserActions


class NoteFindById(Resource, UserActions):
    """Чтение записи из дневника сна по id"""

    @ns_notes.response(**response_model_200)
    @ns_notes.response(**response_model_401)
    @ns_notes.response(**response_model_404)
    @ns_notes.doc(
        description=__doc__,
        params=path_params,
    )
    def get(self, id: int):
        db_note: SleepNoteOrm | None = find_user_note_by_note_id(
            id=id,
            user_id=self.current_user_id,
        )
        if db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
