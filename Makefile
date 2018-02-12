.PHONY: test tox bandit

TOXENVLIST=$(shell awk -F = '/^envlist=/ { print $$2; }' tox.ini)

test: tox bandit

tox:
	tox -e ${TOXENVLIST}

bandit:
	bandit -r scripts gpmplgen tests

~/.pypirc: .pypirc
	@sed -e "s/PYPI_USER/${PYPI_USER}/g" -e "s/PYPI_PASSWORD/${PYPI_PASSWORD}/g" -e "s/PYPITEST_PASSWORD/${PYPITEST_PASSWORD}/g" $< > $@
