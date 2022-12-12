VERSION=v1
DOCKERUSER=jhansisaketa

build:
	docker build -f Dockerfile -t nba-rest .
push:
	docker tag nba-rest jhansisaketa/nba-rest:v1
	docker push jhansisaketa/nba-rest:v1
	docker tag nba-rest jhansisaketa/nba-rest:latest
	docker push jhansisaketa/nba-rest:latest
