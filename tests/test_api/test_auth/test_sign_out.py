import pytest


@pytest.mark.auth
class TestSignOut:

    @pytest.mark.skip(reason="Нет имплементации роута")
    def test_sign_out_200(self):
        pass
