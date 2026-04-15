PYTHON = poetry run python
PYTHON_SHELL = poetry run ipython
DEBUG_PORT = 5678

.PHONY: help install lock shell ipython python-debug debug test test-verbose test-compiler test-tooling test-legacy smoke format lint check run-examples example cli-tokenize cli-parse cli-format cli-debug clean

sd: python-debug
s: ipython
t: python-test

help:
	@Write-Output "Available targets:"
	@Write-Output "  install        - install project dependencies"
	@Write-Output "  lock           - refresh poetry lockfile"
	@Write-Output "  shell          - open a Python REPL in poetry"
	@Write-Output "  ipython        - open IPython in poetry"
	@Write-Output "  debug          - open IPython with debugpy listening"
	@Write-Output "  test           - run all tests"
	@Write-Output "  test-verbose   - run tests with stdout"
	@Write-Output "  test-compiler  - run compiler-focused tests"
	@Write-Output "  test-tooling   - run formatter/debugger tests"
	@Write-Output "  test-legacy    - run legacy compatibility tests"
	@Write-Output "  smoke          - run a small end-to-end CLI smoke check"
	@Write-Output "  format         - run Black"
	@Write-Output "  lint           - run Flake8"
	@Write-Output "  check          - run format, lint, and tests"
	@Write-Output "  run-examples   - run the bundled example"
	@Write-Output "  cli-tokenize   - tokenize a sample jq filter"
	@Write-Output "  cli-parse      - parse a sample jq filter"
	@Write-Output "  cli-format     - format a sample jq filter"
	@Write-Output "  cli-debug      - debug a sample jq filter"
	@Write-Output "  clean          - remove local Python cache folders"

install:
	poetry install

lock:
	poetry lock

shell:
	$(PYTHON)

ipython:
	$(PYTHON_SHELL)

python-debug:
	$(PYTHON_SHELL) --InteractiveShellApp.exec_lines="import debugpy; debugpy.listen(('localhost', 5678))"

debug: python-debug

python-test:
	poetry run pytest -s

test:
	poetry run pytest

test-verbose:
	poetry run pytest -s

test-compiler:
	poetry run pytest tests/test_compiler.py

test-tooling:
	poetry run pytest tests/test_tooling.py

test-legacy:
	poetry run pytest tests/test_automations

smoke:
	$(PYTHON) -m jqtools tokenize ".name | {count: 2}"
	$(PYTHON) -m jqtools parse ".people[] | select(.active)"
	$(PYTHON) -m jqtools format "{name:.user,items:[1,2,3]}"
	$(PYTHON) -m jqtools debug ".name | length"

format:
	poetry run black src tests examples

lint:
	poetry run flake8 src tests examples automations

check: format lint test

run-examples:
	$(PYTHON) examples/basic_usage.py

example: run-examples

cli-tokenize:
	$(PYTHON) -m jqtools tokenize ".name | .age"

cli-parse:
	$(PYTHON) -m jqtools parse ".people[] | select(.active)"

cli-format:
	$(PYTHON) -m jqtools format "{name:.user,items:[1,2,3]}"

cli-debug:
	$(PYTHON) -m jqtools debug "if .age >= 18 then \"adult\" else \"child\" end"

clean:
	Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
