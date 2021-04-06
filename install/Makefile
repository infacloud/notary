all:
	@make help

help:
	@echo -e "Usage : Run make using below stages"
	@echo -e "make build-fedramp-staging\nmake build-fedramp-prod\nmake build-commercial-staging\nmake build-commercial-prod"

clean:
ifneq ($(wildcard ./ct-docker-compose.yml),)
	@echo "Cleaning up the docker-compose files."
	@rm ct-docker-compose.yml
else
	@echo "No files to clean."
endif

os-dependencies:
	#curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64" -o /usr/local/bin/docker-compose
	curl -L "https://github.com/theupdateframework/notary/releases/download/v0.6.1/notary-Linux-amd64" -o /usr/local/bin/notary
	chmod +x /usr/local/bin/notary
	#chmod +x /usr/local/bin/docker-compose
	yum update -y
	yum install -y yum-utils docker-ce docker-compose telnet
	#amazon-linux-extras install docker python3 -y
	service docker start

dependencies:
	@pip3 install -r requirements.txt

docker-stage:
	docker-compose -f ../ct-docker-compose.yml up -d --build
	docker-compose logs mysql signer server

manager:
	@python3 manager.py --action $(action) --environment $(environment)

build-commercial-staging:
	@echo "Building the docker-compose.yml file for commercial  staging environment!"
	@make dependencies
	@make action=build_commerical environment=staging manager
	docker login ct-docker.artifacts.cloudtrust.rocks --username ctci-readbot --password $(JFROG_PASSWORD)
	@make docker-stage

build-commercial-prod:
	@echo "Building the docker-compose.yml file for commercial prod environment!"
	@make dependencies
	@make action=build_commerical environment=prod manager
	docker login ct-docker.artifacts.cloudtrust.rocks --username ctci-readbot --password $(JFROG_PASSWORD)
	@make docker-stage

build-fedramp-prod:
	@echo "Building the docker-compose.yml file for fedramp prod environment!"
	@make dependencies
	@make action=build_fedramp environment=prod manager
	aws ecr get-login-password --region us-gov-east-1 | docker login --username AWS --password-stdin 225142825397.dkr.ecr.us-gov-east-1.amazonaws.com
	@make docker-stage

build-fedramp-staging:
	@echo "Building the docker-compose.yml file for fedramp prod environment!"
	@make dependencies
	@make action=build_fedramp environment=staging manager
	aws ecr get-login-password --region us-gov-east-1 | docker login --username AWS --password-stdin 612675333278.dkr.ecr.us-gov-east-1.amazonaws.com
	@make docker-stage
