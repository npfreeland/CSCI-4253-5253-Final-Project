VERSION=v1
DOCKERUSER=jhansisaketa

build:
	docker build -f Dockerfile -t data-collector .
push:
	docker tag data-collector jhansisaketa/data-collector:v1
	docker push jhansisaketa/data-collector:v1
	docker tag data-collector jhansisaketa/data-collector:latest
	docker push jhansisaketa/data-collector:latest
