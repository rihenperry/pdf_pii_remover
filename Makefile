install:
	docker-compose -f docker-compose.build.yml run --rm install

quick-up:
	docker-compose -f docker-compose.build.yml run --rm quick-up

build:
	docker build --no-cache -t pdf-pii-remover:latest --target pdf-pii-remover .

exec:
	mkdir -p ~/output
	docker run -v ~/output:/home/rihan/pdf-pii-remover/output -it --name pii --rm rihbyne/pdf-pii-remover

tag:
	docker tag pdf-pii-remover:latest rihbyne/pdf-pii-remover:latest

push:
	docker push rihbyne/pdf-pii-remover:latest


