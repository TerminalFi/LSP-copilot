UV_INSTALL_FLAGS :=

.PHONY: all
all:

.PHONY: install
install:
	uv pip install $(UV_INSTALL_FLAGS) -r requirements.txt

.PHONY: install-dev
install-dev:
	uv pip install $(UV_INSTALL_FLAGS) -r requirements-dev.txt

.PHONY: pip-compile
pip-compile:
	uv pip compile --upgrade requirements.in -o requirements.txt
	uv pip compile --upgrade requirements-dev.in -o requirements-dev.txt

.PHONY: ci-check
ci-check:
	@echo "========== check: mypy =========="
	mypy -p plugin
	@echo "========== check: ruff (lint) =========="
	ruff check --diff .
	@echo "========== check: ruff (format) =========="
	ruff format --diff .

.PHONY: ci-fix
ci-fix:
	@echo "========== fix: ruff (lint) =========="
	ruff check --fix .
	@echo "========== fix: ruff (format) =========="
	ruff format .
