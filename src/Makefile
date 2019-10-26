.PHONY: test coverage-unit coverage-e2e

PYTHON=python3.8

test:
	$(PYTHON) -B -m unittest -v

coverage-unit:
	$(PYTHON) -m coverage run tests.py && \
	coverage report && \
	coverage html && \
	firefox htmlcov/index.html

coverage-e2e:
	$(PYTHON) -m coverage run main.py ../examples/*.sil >/dev/null && \
	coverage report && \
	coverage html && \
	firefox htmlcov/index.html

