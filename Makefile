SHELL:=/usr/bin/env bash

APP = rental_app
version = 0.0.1

help:
	@echo "Available options:"
	@echo "........................................................"
	@echo "database                     -   upgrade database to latest"
	@echo "coverage                     -   run test and view coverage"
	@echo "precommit                    -   install precommit to local git hooks"
	@echo "lint                         -   run linter"
	@echo "celery                       -   run celery worker"
	@echo "........................................................"

database:
	flask db upgrade

coverage:
	coverage run -m behave -k
	coverage run --append -m pytest
	coverage report

lint:
	flake8 .
	python setup.py isort

celery:
	celery worker -A rental_app.task.* --concurrency=1 --loglevel=info --workdir=./ --pidfile=./celery-rental_app.pid --logfile=./logs/celery-rental_app.log --detach
