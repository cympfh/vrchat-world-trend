DOCKER_TAG := fastsvelte
HOST := 0.0.0.0
PORT := 8093

build:
	cd web; make build

serve: build
	uvicorn server:app --host $(HOST) --port $(PORT) --reload

build-docker:
	docker build -t $(DOCKER_TAG):latest .

serve-docker: build-docker
	docker run --rm -p $(PORT):$(PORT) $(DOCKER_TAG):latest uvicorn server:app --host $(HOST) --port $(PORT)

batch:
	python batch.py

clean:
	python clean.py

WORLD_ID :=
inspect:
	printf ".headers on\nSELECT * FROM world_popularity WHERE world_id = '$(WORLD_ID)'" | sqlite3 database.sqlite3
