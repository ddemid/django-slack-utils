export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	flake8 slack_utils --ignore=E124,E501,E127,E128,E722
	coverage run --source=slack_utils `which django-admin.py` test tests
	coverage report

publish: clean
	python setup.py sdist
	twine upload dist/*

clean:
	rm -vrf ./build ./dist ./*.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.tgz' -delete