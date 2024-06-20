build:
		docker compose build

up: build
		docker compose up -d

down:
		docker compose down --remove-orphans

test: up
		docker compose run --rm --no-deps --entrypoint=pytest tests

logs:
		docker compose logs --tail=25 api postgres pgadmin

sh:
		docker compose -it api bash

