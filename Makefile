install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml

dev-deps: deps
	pip-compile --resolver=backtracking --extra=dev --output-file=dev-requirements.txt pyproject.toml

fmt:
	cd src && autoflake --remove-all-unused-imports -r -i .
	cd src && isort .
	cd src && black .

lint:
	flake8 src
	mypy src

test:
	cd src && pytest