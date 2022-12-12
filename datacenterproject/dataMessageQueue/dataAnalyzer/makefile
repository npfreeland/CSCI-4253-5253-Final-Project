VERSION=v1
DOCKERUSER=jhansisaketa

build:
	docker build -f Dockerfile -t data-analyzer .
push:
	docker tag data-analyzer jhansisaketa/data-analyzer:v1
	docker push jhansisaketa/data-analyzer:v1
	docker tag data-analyzer jhansisaketa/data-analyzer:latest
	docker push jhansisaketa/data-analyzer:latest
