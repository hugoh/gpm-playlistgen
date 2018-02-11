.PHONY: test tox bandit

test: tox bandit

tox:
	tox

bandit:
	bandit -r scripts gpmplgen tests
