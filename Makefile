.PHONY: install run test clean lint build

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m app.main --reload

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 --exclude=.venv

clean:
	rm -rf $(VENV)

build: lint test