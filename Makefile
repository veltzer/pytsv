.PHONY: all
all:
	pytest tests -qq > /dev/null
	pylint pytsv tests

.PHONY: test
test:
	pytest tests

.PHONY: clean
clean:
	find . -name "*.pyc" -or -name "*.pyo" -delete
	find . -name "__pycache__" -exec rm -rf {} \;
