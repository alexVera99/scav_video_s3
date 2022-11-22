lint:
	./venv/bin/pylint src
	./venv/bin/pydocstyle src
	./venv/bin/pycodestyle --select E,W src
	./venv/bin/mypy src