.PHONY: test tox bandit package deploy check-version

TOXENVLIST=$(shell awk -F = '/^envlist=/ { print $$2; }' tox.ini)

test: tox bandit

tox:
	tox -e ${TOXENVLIST}

bandit:
	bandit -r scripts gpmplgen tests

~/.pypirc: .pypirc
	@sed -e "s/PYPI_USER/${PYPI_USER}/g" -e "s/PYPI_PASSWORD/${PYPI_PASSWORD}/g" -e "s/PYPITEST_PASSWORD/${PYPITEST_PASSWORD}/g" $< > $@

package:
	python setup.py check sdist bdist_wheel --universal

deploy: ~/.pypirc
	twine upload dist/GPM-Playlist-Generator-*.tar.gz dist/GPM_Playlist_Generator-*.whl
