all:
	@make help

help:
	@echo "Usage : Run make using below stages"
	@echo "make build-fedramp-staging\nmake build-fedramp-prod\nmake build-commercial-staging\nmake build-commercial-prod"

clean:
ifneq ($(wildcard ./ct-docker-compose.yml),)
	@echo "Cleaning up the docker-compose files."
	@rm ct-docker-compose.yml
else
	@echo "No files to clean."
endif

dependencies:
	@pip3 install -r requirements.txt

docker-stage:
	#docker-compose -f ct-docker-compose.yml up --build
	@echo "Running docker-compose"

manager:
	@python3 manager.py --action $(action) --environment $(environment)

build-commercial-staging:
	@echo "Building the docker-compose.yml file for commercial  staging environment!"
	@make dependencies
	@make action=build_commerical environment=staging manager
	@make docker-stage

build-commercial-prod:
	@echo "Building the docker-compose.yml file for commercial prod environment!"
	@make dependencies
	@make action=build_commerical environment=prod manager
	@make docker-stage

build-fedramp-prod:
	@echo "Building the docker-compose.yml file for fedramp prod environment!"
	@make dependencies
	@make action=build_fedramp environment=prod manager
	@make docker-stage

build-fedramp-staging:
	@echo "Building the docker-compose.yml file for fedramp prod environment!"
	@make dependencies
	@make action=build_fedramp environment=staging manager
	@make docker-stage
