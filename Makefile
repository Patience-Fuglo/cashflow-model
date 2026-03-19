PYTHON ?= python3

.PHONY: test test-all

test test-all:
	$(PYTHON) -m tests
