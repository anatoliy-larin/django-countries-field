django-countries-field
=====

[![Build Status](https://travis-ci.org/anatoliy-larin/django-countries-field.png?branch=master)](https://travis-ci.org/anatoliy-larin/django-countries-field)

Django model field which can store multiple selected countries.

Requirements
=====
* Django>=1.4.0,<1.6.0
* django-bitfield>=1.6.0,<1.7.0
* pycountry>=1.2.0,<1.3.0

Installation
=====

Install it with pip (or easy_install):

```pip install django-countries-field```


Usage
=====

```
# coding: utf-8
from django.db import models
from countries_field.fields import CountriesField


class TestCountriesModel(models.Model):
    countries = CountriesField()
```

More example, see: `countries_field/tests/tests.py`
