clean: |
	sh scripts/clean.sh

create-catalogue-migration-%: |
	@read -p "Enter migration message: " MESSAGE; \
	docker compose -f docker-compose-$*.yaml \
	run --rm migrations-catalogue-$* /bin/bash -c \
	"alembic -c migrations/alembic/alembic.ini revision --autogenerate -m '$$MESSAGE'"

apply-catalogue-migrations-%: |
	docker compose run --rm migrations-catalogue-$*

init-postgres-%: |
	echo "deploy container" && \
	docker compose -f docker-compose-$*.yaml \
	up -d postgres-catalogue-$* && \
	sleep 2s && \
	echo "apply migrations" && \
	docker compose -f docker-compose-$*.yaml \
	run --rm migrations-catalogue-$* && \
	sleep 2s && \
	echo "check tables" && \
	docker compose -f docker-compose-$*.yaml \
	exec postgres-catalogue-$* psql -U catalogue_app -d catalogue -c "\dt"

init-localstack-%: |
	echo "deploy container" && \
	docker compose -f docker-compose-$*.yaml \
	up -d localstack-catalogue-$* && \
	sleep 2s && \
	echo "apply terraform" && \
	terraform -chdir=infra/terraform apply --auto-approve && \
	echo "validate resources" && \
	docker compose -f docker-compose-$*.yaml \
	exec localstack-catalogue-$* awslocal sqs list-queues

init-catalogue-%: |
	make init-postgres-$* && \
	make init-localstack-$* && \
	docker compose -f docker-compose-$*.yaml \
	up -d catalogue-app-$*

down-catalogue-%: |
	docker compose -f docker-compose-$*.yaml down -v

test-catalogue:
	docker compose -f docker-compose-test.yaml run --rm catalogue-tests && \
	docker compose -f docker-compose-test.yaml down -v \

test-catalogue-bdd:
	make init-catalogue-test && \
	docker compose -f docker-compose-test.yaml \
	run --rm catalogue-bdd && \
	make down-catalogue-test
