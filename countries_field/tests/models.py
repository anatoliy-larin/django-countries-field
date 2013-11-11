# coding: utf-8

from django.db import models
from tools.countries_field.fields import CountriesField


class TestCountriesModel(models.Model):
    countries = CountriesField()