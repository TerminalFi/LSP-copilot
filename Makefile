.PHONY: all
all:

# ---- #
# deps #
# ---- #

.PHONY: install-all
install-all:
	uv sync --all-groups

.PHONY: install
install:
	uv sync --no-dev

.PHONY: install-dev
install-dev:
	uv sync --dev

.PHONY: pip-upgrade
pip-upgrade:
	uv sync --all-groups --upgrade

# -- #
# CI #
# -- #

ci-base-cmd = uv run --dev

.PHONY: ci-check
ci-check:
	@echo "========== check: mypy =========="
	$(ci-base-cmd) mypy -p plugin
	@echo "========== check: ruff (lint) =========="
	$(ci-base-cmd) ruff check --diff .
	@echo "========== check: ruff (format) =========="
	$(ci-base-cmd) ruff format --diff .

.PHONY: ci-fix
ci-fix:
	@echo "========== fix: ruff (lint) =========="
	$(ci-base-cmd) ruff check --fix .
	@echo "========== fix: ruff (format) =========="
	$(ci-base-cmd) ruff format .

.PHONY: ci-fix-unsafe
ci-fix-unsafe:
	@echo "========== fix: ruff (lint unsafe) =========="
	$(ci-base-cmd) ruff check --fix --unsafe-fixes .
	@echo "========== fix: ruff (format) =========="
	$(ci-base-cmd) ruff format .
