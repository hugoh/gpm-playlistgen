.PHONY: test tox test-ci tox-ci bandit

test: tox bandit

tox: # Dev environment
	tox -e py27,py36

test-ci: tox-ci bandit

tox-ci: # Fot the CI environment
	tox -e py27,py35

bandit:
	bandit -r scripts gpmplgen tests
