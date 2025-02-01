.PHONY: build run test coverage clean docker-build docker-run

# Docker commands
docker-build:
	docker build -t customer-order-service .

docker-run:
	docker run -p 8000:8000 customer-order-service

# Development commands
install:
	pip install -r requirements.txt

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete