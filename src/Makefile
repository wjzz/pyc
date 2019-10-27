.PHONY: test coverage-unit coverage-e2e

PYTHON=python

test:
	$(PYTHON) -B -m unittest -v


coverage:
	$(PYTHON) -m coverage run tests.py
	for file in ../examples/*.sil; do $(PYTHON) -m coverage run -a main.py $$file >/dev/null 2>/dev/null; done
	for file in ../errors/*.sil; do $(PYTHON) -m coverage run -a main.py $$file >/dev/null 2>/dev/null; done || true
	coverage report && \
	coverage html && \
	firefox htmlcov/index.html

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

