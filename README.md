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
    - Аутентификация | эндпоинты
      - вход
      - аккаунт пользователя
      - регистрация
      - выход (активный токен должен быть забанен)
        - Реализация sign-out, через хранилище в cache и RedisCache
        - 
- в абстракциях сделать только абстрактные методы - это будет интерфейсом
- Alembic
  - Добавить зависимость
  - Создание таблиц/схем основной БД [Вручную]
- ORMNote
  - Протестировать каскадное удаление всех записей пользователя при удалении 
    пользователя (all, delete-orphan)
- Кеширование запросов
- Создание ключей public и private keys для jwt 
  - при тестировании
  - при развертывании на windows

- Зависимости:
- dev+ pre-committer
- dev+ ipython
- CI/CD
