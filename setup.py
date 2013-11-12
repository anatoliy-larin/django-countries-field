#!/usr/bin/env python

from setuptools import setup, find_packages

# https://github.com/msabramo/virtualenv/commit/ddd0aa02cf822fc690ff9c4bfead70c3e6767eee
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='django-countries-field',
    version='0.1.0',
    author='RUTUBE',
    author_email='devel@rutube.ru',
    url='https://github.com/anatoliy-larin/django-countries-field',
    description='CountriesField in Django',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django>=1.4.0,<1.6.0',
        'django-bitfield>=1.6.0,<1.7.0',
        'pycountry>=1.2.0,<1.3.0',
    ],
    setup_requires=[
        'nose>=1.0',
    ],
    tests_require=[
        'django-nose>=0.1.3',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
)
