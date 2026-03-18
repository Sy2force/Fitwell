.PHONY: install migrate seed run test clean build

install:
	pip install -r backend/requirements.txt

migrate:
	python3 backend/manage.py migrate

seed:
	python3 backend/manage.py seed_db
	python3 backend/manage.py seed_exercises
	python3 backend/manage.py seed_blog
	python3 backend/manage.py seed_badges
	python3 backend/manage.py seed_recipes

run:
	python3 backend/manage.py runserver

test:
	python3 backend/manage.py test api web

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	chmod +x backend/build_files.sh
	./backend/build_files.sh
