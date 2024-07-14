clean: |
	sh scripts/clean.sh

create-catalogue-migration: |
	@read -p "Enter migration message: " MESSAGE; \
	docker compose run --rm catalogue-migrations /bin/bash -c \
	"alembic -c migrations/alembic/alembic.ini revision --autogenerate -m '$$MESSAGE'"

apply-catalogue-migrations: |
	docker compose run --rm catalogue-migrations

init-postgres: |
	echo "deploy container" && \
	docker compose up -d postgres-db && \
	sleep 2s && \
	echo "apply migrations" && \
	docker compose run --rm catalogue-migrations && \
	sleep 2s && \
	echo "check tables" && \
	docker compose exec postgres-db psql -U catalogue_app -d catalogue -c "\dt"

init-localstack: |
	echo "deploy container" && \
	docker compose up -d localstack && \
	sleep 2s && \
	echo "apply terraform" && \
	terraform -chdir=infra/terraform apply --auto-approve && \
	echo "validate resources" && \
	docker compose exec localstack awslocal sqs list-queues

init-catalogue: |
	docker compose up -d catalogue

test-catalogue:
	docker compose -f docker-compose-test.yaml run --rm catalogue-test && \
	docker compose -f docker-compose-test.yaml down -v \

test-catalogue-bdd:
	make init-postgres && \
	make init-localstack && \
	make init-catalogue && \
	docker compose run --rm catalogue-bdd && \
	docker compose down -v
