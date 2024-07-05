build:
		docker compose -f flask_app.yml -f postgres.yml build
up: build
		docker compose -f flask_app.yml -f postgres.yml up -d
down:
		docker compose -f flask_app.yml -f postgres.yml down --remove-orphans
test: up
		docker compose -f flask_app.yml -f postgres.yml run --rm --no-deps --entrypoint="pytest tests/" api
logs:
		docker compose -f flask_app.yml -f postgres.yml logs --tail=25 api postgres pgadmin
sh:
		docker run -it api bash
bi:
		black . && isort .