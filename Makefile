PROJECT_NAME := data
PROJECT_HOME := $(shell pwd)
SHARED := $(if $(SHARED_VOLUME), -v $(SHARED_VOLUME):$(SHARED_VOLUME),)


docker:
	docker build -t ${PROJECT_NAME}_dev -f docker/Dockerfile .

up_db:
	docker-compose -f docker/docker-compose.yml up -d mongo

run:
	set -a
	export PROJECT_HOME=${PROJECT_HOME} && docker-compose -f docker/docker-compose.yml up -d server
	# docker run -it --name ${PROJECT_NAME}_dev_${USER} ${SHARED} -v ${PROJECT_HOME}/src:/src/ -v ${PROJECT_HOME}:/workspace/ -v /var/run/docker.sock:/var/run/docker.sock:ro -p 5555:5555 ${PROJECT_NAME}_dev

.PHONY: docker run