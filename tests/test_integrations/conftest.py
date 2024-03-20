import json
import os

import pytest

from tests.conftest import app


@pytest.fixture
def main_page_info(client):
    static_dir = client.application.static_folder
    with open(f"{static_dir}/content/main.json", "r") as f:
        return json.load(f)


# @pytest.fixture(
#     autouse=True,
#     scope='function'
# )
# def prepare_database(app):
    # assert app.config.get("TESTING") is True
    # assert app.config.get("DB_NAME") == os.environ.get("DB_NAME")
