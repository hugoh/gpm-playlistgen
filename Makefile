.PHONY: test

test:
	python -m unittest discover
	bandit -r .
