import os
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_dairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APP_MODE = os.getenv('FLASK_ENV')

Errors = {
    'add': 'При добавлении записи в дневник произошла ошибка',
    'update': 'При обновлении записи в дневнике произошла ошибка',
    'value': 'Неподходящее значение',
    'syntax': 'Неподходящий формат',
    'type': 'Неподходящий тип данных',
    'database': 'При обращении к базе данных произошла ошибка',
    'file': 'Файл не был найден',
    'import': 'При импортировании произошла ошибка',
    'other': 'Прочая ошибка'
}
