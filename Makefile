.PHONY: all
all: fix

.PHONY: check
check:
	# mypy -p plugin
	flake8 .
	pycln --config pyproject.toml --check .
	black --check .
	isort --check .

.PHONY: fix
fix:
	pycln --config pyproject.toml .
	black .
	isort .
