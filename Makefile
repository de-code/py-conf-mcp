#!/usr/bin/make -f

DOCKER_COMPOSE_DEV = docker compose
DOCKER_COMPOSE_CI = docker compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

PYTEST_WATCH_MODULES = tests/unit_tests

MCP_METHOD = tools/list


.require-%:
	@ if [ "${${*}}" = "" ]; then \
			echo "Environment variable $* not set"; \
			exit 1; \
	fi


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi


venv-create:
	python3 -m venv $(VENV)


venv-activate:
	chmod +x venv/bin/activate
	bash -c "venv/bin/activate"


dev-install:
	$(PIP) install --disable-pip-version-check \
		-r requirements.build.txt \
		-r requirements.txt \
		-r requirements.dev.txt \


dev-venv: venv-create dev-install


dev-flake8:
	$(PYTHON) -m flake8 py_conf_mcp

dev-pylint:
	$(PYTHON) -m pylint py_conf_mcp

dev-mypy:
	$(PYTHON) -m mypy --check-untyped-defs py_conf_mcp

dev-lint: dev-flake8 dev-pylint dev-mypy


dev-unit-tests:
	$(PYTHON) -m pytest

dev-watch:
	$(PYTHON) -m pytest_watcher \
		--runner=$(VENV)/bin/python \
		. \
		-m pytest -vv $(PYTEST_WATCH_MODULES)


dev-test: dev-lint dev-unit-tests


dev-start:
	CONFIG_FILE=config/server.yaml \
		$(PYTHON) -m py_conf_mcp \
			--transport=sse \
			--host=localhost \
			--port=8080


dev-mcp-inspect-cli:
	npx @modelcontextprotocol/inspector \
		--cli \
		'http://localhost:8080' \
		--method "$(MCP_METHOD)"


dev-mcp-inspect-ui:
	npx @modelcontextprotocol/inspector



build:
	$(DOCKER_COMPOSE) build

flake8:
	$(DOCKER_COMPOSE) run --rm py-conf-mcp \
		python3 -m flake8 py_conf_mcp

pylint:
	$(DOCKER_COMPOSE) run --rm py-conf-mcp \
		python3 -m pylint py_conf_mcp

mypy:
	$(DOCKER_COMPOSE) run --rm py-conf-mcp \
		python3 -m mypy --check-untyped-defs py_conf_mcp

lint: flake8 pylint mypy


unit-tests:
	$(DOCKER_COMPOSE) run --rm py-conf-mcp \
		python3 -m pytest


test: lint unit-tests


start:
	$(DOCKER_COMPOSE) up -d

logs:
	$(DOCKER_COMPOSE) logs -f

stop:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down -v


ci-build:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" build

ci-lint:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" lint


ci-unit-tests:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" unit-tests
