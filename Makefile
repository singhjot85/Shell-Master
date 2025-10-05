# PYTHON_SHELL = poetry run python
PYTHON_SHELL = poetry run ipython
DEBUG_PORT = 5678

.PHONY: ipd, i, t

ipd: python-debug
i: ipython
t: python-test

ipython:
	$(PYTHON_SHELL)

python-debug:
	$(PYTHON_SHELL) --InteractiveShellApp.exec_lines="import debugpy; debugpy.listen(('localhost', 5678))"

python-test:
	poetry run pytest -s