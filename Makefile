.PHONY: all

all:
	@python -m pylint -E pytsv

clean:
	find . -name "*.pyc" -or -name "*.pyo" -delete
	find . -name "__pycache__" -exec rm -rf {} \;
