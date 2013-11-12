# coding: utf-8
from django.db import models

from countries_field.fields import CountriesField


class TestCountriesModel(models.Model):
    """ Test model
    """
    countries = CountriesField()
