.PHONY: test unittest bandit

test: unittest bandit

unittest:
	python -m unittest discover

bandit:
	bandit -r .
