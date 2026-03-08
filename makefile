.PHONY: test test-markers test-confirmations test-perissions

test:
	python manage.py test maps.tests

test-markers:
	python manage.py test maps.tests.test_markers

test-confirmations:
	python manage.py test maps.tests.test_confirmations

test-permissions:
	python manage.py test maps.tests.test_permissions
