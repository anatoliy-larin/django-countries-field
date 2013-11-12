# coding: utf-8
import unittest
from django.conf import settings
from django.db.models import loading
from django.test import TestCase

from countries_field.fields import CountriesValue
from models import TestCountriesModel


class CountriesFieldTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """ Подключает тестовые модели и синкает базу с ними """
        cls._installed_apps = settings.INSTALLED_APPS
        settings.INSTALLED_APPS.append("countries_field.tests")
        from django.core.management import call_command
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

    @classmethod
    def tearDownClass(cls):
        """ Отключаем тестовое приложение. """
        settings.INSTALLED_APPS = cls._installed_apps
        loading.cache.loaded = False

    def setUp(self):
        self.initial_countries = ["ru", "UA", "Au"]
        self.testee = TestCountriesModel.objects.create(
            countries=self.initial_countries)

    def testCreate(self):
        """ Позволяет задать список стран при инициализации. """
        check = TestCountriesModel.objects.get(pk=self.testee.pk)
        self.assertEqual(self.initial_countries, check.countries)

    def testSetNewValue(self):
        """ Позволяет задать новый список стран. """
        new_value = ["gb", "us", "au"]
        for expected in (new_value, CountriesValue(countries=new_value)):
            self.testee.countries = new_value
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(expected, check.countries)

    def setEmptyList(self):
        """ Пустой список сбрасывает все установлденные страны. """
        new_value = ()
        self.testee.countries = new_value
        self.testee.save()
        check = TestCountriesModel.objects.get(pk=self.testee.pk)
        self.assertEqual(new_value, check.countries)

    def testAddCountries(self):
        """ Позволяет дополнить список стран. """
        countries = ["Gb", "US"]
        for added in (countries, CountriesValue(countries=countries)):
            self.testee.countries |= added
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(list(self.initial_countries) + countries,
                             check.countries)

    def testRemoveCountries(self):
        """ Позволяет исключить список стран. """
        expected = self.initial_countries[:]
        delete_country = expected.pop()
        expected.reverse()
        for deleted in ((delete_country,),
                        CountriesValue(countries=(delete_country,))):
            self.testee.countries -= deleted
            self.testee.save()
            check = TestCountriesModel.objects.get(pk=self.testee.pk)
            self.assertEqual(expected, check.countries)

    def testContains(self):
        """ Позволяет проверить вхождение списка стран. """
        self.assertTrue("ru" in self.testee.countries)

    def testEqual(self):
        """ Сравнение работает парвильно для одинаковых списков стран. """
        for expected in (self.initial_countries,
                         CountriesValue(countries=self.initial_countries)):
            self.assertEquals(expected, self.testee.countries)

    def testNotEqual(self):
        """ Сравнение работает правильно для разных списков стран. """
        countries = self.initial_countries[:-1]
        for expected in (countries, CountriesValue(countries=countries)):
            self.assertNotEquals(expected, self.testee.countries)

    @unittest.expectedFailure
    def testLookup(self):
        check = TestCountriesModel.objects.get(countries=["ru"])
