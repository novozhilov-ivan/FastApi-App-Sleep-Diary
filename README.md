# project_sleep_diary

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```


# TODO
## DDD
- FastApi:
    - General response schemas:
      - 400: 
      - 401:
      - 404:
      - 415:
      - 422:
    - Endpoints:
      - /add_note
        - Определить форму ответа для 201
          - body +-?
          - header location '/api/notes/<uuid:43fgf...>'
        - Тесты:
          - 201: Проверка body/location
    - NoteEntity
    - Сервис авторизации:
    - Переписать
    - UserRepo
    - Схема Note
      - Отделить owner_id 
      - Отделить мета информацию
    - Схемы User'ов
    - Как использовать с application?
    - Реализация sign-out, через хранилище в cache и RedisCache
    - Создание в памяти public и private keys для шифрования при тестировании
  - Рефакторинг
    - BaseDatabase и тесты для FakeDatabase.
    - Установить Аннотацию типа у session в Database. Сейчас pycharm не понимает.
    - Протестировать каскадное удаление записей при удалении user. (all, 
      delete-orphan) в таблице 'users' мб нужно выставить.
    - Заменить вызовы переиспользуемых объектов Dependency Injector Container.
  - Diary + Week взаимодействие.
    - Diary < метод make_diary() для формирования словаря/json с записями
    разделенными неделями, со своими сортировками
  - Зависимости:
   - prod+ Dependency Injector
   - dev+ pre-committer
   - dev+ ipython
  - CI/CD
