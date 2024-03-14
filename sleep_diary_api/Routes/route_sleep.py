from flask_restx import Resource, Namespace

sleep_page = Namespace('api')


@sleep_page.route("/sleep")
class SleepPage(Resource):
    def get(self):
        return [
            {}
        ]
