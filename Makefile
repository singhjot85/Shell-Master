PYTHON = poetry run python
DEBUG_PORT = 5678

python:
	$(PYTHON)

python-debug:
	$(PYTHON) -c "import debugpy; debugpy.listen(('localhost', $(DEBUG_PORT))); print('debugpy listening on port $(DEBUG_PORT)'); import code; code.interact(local=globals())"
