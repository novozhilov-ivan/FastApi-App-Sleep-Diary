build:
		docker compose build

up: build
		docker compose up -d
		#docker compose up -d --env-file .env

down:
		docker compose down --remove-orphans

test: up
		docker compose run --rm --no-deps --entrypoint=pytest api

logs:
		docker compose logs --tail=25 api postgres pgadmin

sh:
		docker compose -it api bash

