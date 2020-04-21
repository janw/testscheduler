DOCKER=docker
DOCO=docker-compose
PYTHON=python3
YARN=yarn

VENV_DIR=$(CURDIR)/.venv
FRONTEND_DIR=$(CURDIR)/frontend
REQ_FILE_DEV=$(CURDIR)/requirements-dev.txt

PIP=$(VENV_DIR)/bin/pip
PY=$(VENV_DIR)/bin/python
HONCHO=$(VENV_DIR)/bin/honcho

deps:
	$(YARN) --cwd $(FRONTEND_DIR) install
	test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install -r $(REQ_FILE_DEV)

serve:
	$(HONCHO) start

build:
	$(DOCKER) build -t janwh/testscheduler .

up:
	$(DOCO) up

buildup: build up

test:
	$(PY) -m pytest tests/backend --cov=testscheduler
