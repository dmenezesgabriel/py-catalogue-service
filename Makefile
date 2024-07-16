clean:
	sh scripts/clean.sh

create-catalogue-migration-%:
	@read -p "Enter migration message: " MESSAGE; \
	docker compose -f docker-compose-$*.yaml \
	run --rm migrations-catalogue-$* /bin/bash -c \
	"alembic -c migrations/alembic/alembic.ini revision --autogenerate -m '$$MESSAGE'"

apply-catalogue-migrations-%:
	docker compose run --rm migrations-catalogue-$*

init-postgres-%:
	docker compose -f docker-compose-$*.yaml \
	up -d postgres-catalogue-$* && \
	sleep 2s && \
	docker compose -f docker-compose-$*.yaml \
	run --rm migrations-catalogue-$* && \
	sleep 2s && \
	docker compose -f docker-compose-$*.yaml \
	exec postgres-catalogue-$* psql -U catalogue_app -d catalogue -c "\dt"

init-localstack-%:
	docker compose -f docker-compose-$*.yaml \
	up -d localstack-catalogue-$* && \
	sleep 2s && \
	terraform -chdir=infra/terraform/localstack init -var-file=environments/$*/$*.tfvars && \
	terraform -chdir=infra/terraform/localstack apply -var-file=environments/$*/$*.tfvars --auto-approve && \
	docker compose -f docker-compose-$*.yaml \
	exec localstack-catalogue-$* awslocal sqs list-queues

start-catalogue-%:
	docker compose -f docker-compose-$*.yaml up -d catalogue-app-$*

init-catalogue-%:
	make init-postgres-$* && \
	make init-localstack-$* && \
	make start-catalogue-$*

down-catalogue-%:
	docker compose -f docker-compose-$*.yaml down -v

catalogue-unit-tests:
	docker compose -f docker-compose-test.yaml run --rm catalogue-unit-tests

catalogue-integration-tests:
	docker compose -f docker-compose-test.yaml run --rm catalogue-integration-tests && \
	docker compose -f docker-compose-test.yaml down -v \

start-catalogue-bdd:
	docker compose -f docker-compose-test.yaml \
	run --rm catalogue-bdd

init-catalogue-bdd:
	make init-catalogue-test && \
	make start-catalogue-bdd && \
	make down-catalogue-test

start-catalogue-load:
	docker compose -f docker-compose-test.yaml \
	run --rm catalogue-load

init-catalogue-load:
	make init-catalogue-test && \
	make start-catalogue-load && \
	make down-catalogue-test

build-catalogue-prod:
	docker build --no-cache -t py-order-system-catalogue .
