PROJECT_NAME := data
PROJECT_HOME := $(shell pwd)
SHARED := $(if $(SHARED_VOLUME), -v $(SHARED_VOLUME):$(SHARED_VOLUME),)


docker:
	docker build -t ${PROJECT_NAME}_dev -f docker/Dockerfile .

run:
	docker rm ${PROJECT_NAME}_dev_${USER} || true
	docker run -it --name ${PROJECT_NAME}_dev_${USER} ${SHARED} -v ${PROJECT_HOME}:/workspace/ -v /var/run/docker.sock:/var/run/docker.sock:ro -p 5555:5555 ${PROJECT_NAME}_dev

.PHONY: docker run