export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
export COMPOSE_IGNORE_ORPHANS=1


build:
	docker compose -f sleep_diary.yml -f postgres.yml build

pull-postgres:
	docker compose -f postgres.yml pull
pull-pgadmin:
	docker compose -f pgadmin.yml up pull
pull-all: pull-postgres pull-pgadmin

up-postgres:
	docker compose -f postgres.yml up -d
up-pgadmin:
	docker compose -f pgadmin.yml up -d --no-recreate
up: build
	docker compose -f sleep_diary.yml -f postgres.yml up -d
up-all: build up-postgres up-pgadmin
	docker compose -f sleep_diary.yml -f postgres.yml up -d

down:
	docker compose -f sleep_diary.yml -f postgres.yml down
down-all:
	docker compose -f sleep_diary.yml -f postgres.yml down --remove-orphans

unit: up
	docker compose -f sleep_diary.yml -f postgres.yml run --rm --entrypoint="pytest tests/unit" sleep_diary
integration: up
	docker compose -f sleep_diary.yml -f postgres.yml run --rm --entrypoint="pytest tests/integration" sleep_diary
e2e: up
	docker compose -f sleep_diary.yml -f postgres.yml run --rm --entrypoint="pytest tests/e2e" sleep_diary
all: up
	docker compose -f sleep_diary.yml -f postgres.yml run --rm --entrypoint="pytest" sleep_diary

logs:
	docker compose -f sleep_diary.yml -f postgres.yml logs --tail=35 sleep_diary
logs-pgadmin:
	docker compose -f pgadmin.yml logs --tail=25 pgadmin
sh:
	docker exec -it sleep_diary bash
migrate:
	docker exec -it sleep_diary alembic -c src/alembic.ini upgrade head
all-cov:
	coverage run -m pytest
	coverage report -m
open-cov: all-cov
	coverage html
	xdg-open coverage_html_report/index.html
clean-cov:
	rm -rf \
		coverage_html_report \
		coverage.xml \
		.coverage \
		.pytest_cache
