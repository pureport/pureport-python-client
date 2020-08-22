.PHONY: clean
clean:
	if [ -d build ]; then rm -rf build; fi
	if [ -d dist ]; then rm -rf dist; fi
	if [ -d pureport_client.egg-info ]; then rm -rf pureport_client.egg-info; fi
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	coverage erase
	if [ -d .tox ]; then rm -rf .tox; fi

test: clean
	tox
