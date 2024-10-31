export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
export COMPOSE_IGNORE_ORPHANS=1


build:
	docker compose -f app.yml -f postgres.yml build
up-postgres:
	docker compose -f postgres.yml up -d
pgadmin:
	docker compose -f pgadmin.yml up -d --no-recreate
up: build
	docker compose -f app.yml -f postgres.yml up -d
up-all: build pgadmin
	docker compose -f app.yml -f postgres.yml up -d
down: down-postgres
	docker compose -f app.yml down
down-postgres:
	docker compose -f postgres.yml down
down-all:
	docker compose -f app.yml -f postgres.yml down --remove-orphans
unit: up
	docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/unit" api
integration: up
	docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/integration" api
e2e: up
	docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/e2e" api
all: up
	docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest --dist=worksteal -n 4" api
logs:
	docker compose -f app.yml -f postgres.yml logs --tail=25 api postgres
sh:
	docker exec -it api bash
bi:
	black . && isort .
upgrade-to-head:
	docker exec -it api alembic upgrade head
