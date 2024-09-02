from http import HTTPStatus

from flask.testing import FlaskClient

from src.infrastructure.orm import ORMUser


def test_add_note_201(client: FlaskClient, user: ORMUser):
    data = {
        "bedtime_date": "2020-12-12",
        "went_to_bed": "01:00",
        "fell_asleep": "03:00",
        "woke_up": "11:00",
        "got_up": "13:00",
        "no_sleep": "01:00",
        "owner_id": f"{user.oid}",
    }
    response = client.post(
        path="api/notes",
        json=data,
        # auth=jwt_access,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json is None
