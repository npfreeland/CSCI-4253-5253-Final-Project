VERSION=v1
DOCKERUSER=jhansisaketa

build:
	docker build -f Dockerfile -t model-server .
push:
	docker tag model-server jhansisaketa/model-server:v1
	docker push jhansisaketa/model-server:v1
	docker tag model-server jhansisaketa/model-server:latest
	docker push jhansisaketa/model-server:latest
