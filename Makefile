.PHONY: test tox bandit

TOXENVLIST=$(shell awk -F = '/^envlist=/ { print $$2; }' tox.ini)

test: tox bandit

tox:
	tox -e ${TOXENVLIST}

bandit:
	bandit -r scripts gpmplgen tests
