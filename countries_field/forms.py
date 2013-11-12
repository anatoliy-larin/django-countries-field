# coding: utf-8
import gettext
from django.conf import settings
from django.forms import MultipleChoiceField
import pycountry
from countries_field.fields import countries


class CountriesFormField(MultipleChoiceField):
    """ Поле формы для поддержки поля модели CountriesField.
    """

    def __init__(self, choices=None, *args, **kwargs):
        """ Задает в choices список стран по стандарту iso3166.
        :param choices: Переопределяет набор использыемых стран.
        :param args:
        :param kwargs:
        :return:
        """
        if choices is None:
            choices = self.generate_countries_choices()
        super(CountriesFormField, self).__init__(choices=choices, *args,
                                                 **kwargs)

    def generate_countries_choices(self):
        """ Генерирует choices для стран по iso3166. """
        choices = ((c.alpha2, c.name) for c in countries)
        if settings.USE_L10N:
            lang = settings.LANGUAGE_CODE[0:2]
            locale = gettext.translation('iso3166', pycountry.LOCALES_DIR,
                                         languages=[lang])
            choices = ((k,  locale.ugettext(v)) for k, v in choices)

        return sorted(choices, key=lambda x: x[1])
