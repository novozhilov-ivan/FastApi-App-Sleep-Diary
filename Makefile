DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .docker.env
API_FILE = docker_compose/docker-compose.yaml
API_CONTAINER = api
PGADMIN_CONTAINER = pgadmin


.PHONY: api
api:
	${DC} -f ${API_FILE} ${ENV} up --build -d

.PHONY: down
down:
	${DC} -f ${API_FILE} down

.PHONY: logs
logs:
	${LOGS} ${API_CONTAINER} -f

.PHONY: logs_pgadmin
logs_pgadmin:
	${LOGS} ${PGADMIN_CONTAINER} -f

.PHONY: sh
sh:
	${EXEC} ${API_CONTAINER} bash

.PHONY: test
test:
	${EXEC} ${API_CONTAINER} pytest -s