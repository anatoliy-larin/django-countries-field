#!/usr/bin/env python
import sys
from optparse import OptionParser

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                #'ENGINE': 'django.db.backends.mysql',
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'country_field_test',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },

        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'countries_field',
            'countries_field.tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
    )


from django_nose import NoseTestSuiteRunner


def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['countries_field']

    test_runner = NoseTestSuiteRunner(**kwargs)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store',
                      default=1, type=int)
    parser.add_options(NoseTestSuiteRunner.options)
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)
