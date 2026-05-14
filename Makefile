.PHONY: start stop build

all: start

start:
	docker compose -f src/docker-compose.yml up -d

stop:
	docker compose -f src/docker-compose.yml down

build:
	docker compose -f src/docker-compose.yml up --build -d
