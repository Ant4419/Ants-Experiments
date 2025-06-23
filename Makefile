# Makefile for Ants-Experiments

up:
	bash setup.sh

down:
	cd docker && docker-compose down

logs:
	cd docker && docker-compose logs -f

build:
	cd docker && docker-compose build

test:
	pytest tests/

clean:
	rm -rf .venv __pycache__
	cd docker && docker-compose down -v
