# Load App Settings
# app.config.from_pyfile('config.py')
from .config import *
# Views необходимо импортировать после app = Flask(__name__),
# иначе ошибка из-за зацикленности наследования
from app import routes

# Смысл нахождения этой хуйни? - если мы не в production, то можем читать данный файл(как?)
# If production mode
if (os.getenv('FLASK_ENV')) == "production":
    pass
