name = recyclus-batch
user ?= ylivnat

all : clean push

status:
	git status

build:
	docker build -t $(user)/$(name) .


push: build
	docker push $(user)/$(name)


clean:
	docker image rm $(user)/$(name)
