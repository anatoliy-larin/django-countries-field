# coding: utf-8
from django.db import models
from django.db.models.fields.subclassing import Creator

from bitfield.models import BitField, MAX_FLAG_COUNT
import pycountry


countries = pycountry.countries
alpha2_index = [c.alpha2 for c in countries]
alpha2_map = {c: p for p, c in enumerate(alpha2_index)}

# Допустимые биты для хранения стран.
VALID_BINARY_MASK = (1 << MAX_FLAG_COUNT) - 1


def countries_to_bin(countries):
    binaries = [0, 0, 0, 0]
    for c in countries:
        c_num = alpha2_map[c.upper()]
        byte_num = c_num / MAX_FLAG_COUNT
        bit_num = c_num % MAX_FLAG_COUNT
        binaries[byte_num] |= 1 << bit_num
    return binaries


def bin_to_countries(binaries):
    """ Превращает все установленные биты в первых 4-х элементах списка в
    список стран.
    :param binaries: Список из 4 элементов шириной MAX_FLAG_COUNT каждый
    :return: Список 2-х буквенных кодов стран

    """
    countries = []
    for byte_num in xrange(4):
        byte = binaries[byte_num] & VALID_BINARY_MASK
        byte_shift = byte_num * MAX_FLAG_COUNT
        bit_num = 0
        while byte:
            if byte & 0b1:
                countries.append(alpha2_index[byte_shift + bit_num])
            byte >>= 1
            bit_num += 1
    return countries


class CountriesValue(object):
    """ Представление набора заданых стран.
    """
    def __init__(self, binaries=None, countries=None):
        self.binaries = [int(b) & VALID_BINARY_MASK
                         for b in (binaries or [0, 0, 0, 0])]
        if isinstance(countries, (list, tuple)):
            countries = countries_to_bin(countries)
            for i in xrange(4):
                self.binaries[i] |= countries[i]

    def __iter__(self):
        for c in bin_to_countries(self.binaries):
            yield c

    def __getitem__(self, item):
        return self.binaries[item]

    def __eq__(self, other):
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        if isinstance(other, CountriesValue):
            other = other.binaries
        return self.binaries == other

    def __repr__(self):
        return "%s (%s)" % (self.__class__, bin_to_countries(self.binaries))

    def __or__(self, other):
        """ Объединяет списки стран.
        :param other: список 2-х буквенных кодов стран
        :return: CountriesValues

        """
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        result = [0, 0, 0, 0]
        for i in xrange(4):
            result[i] = self.binaries[i] | other[i]
        return CountriesValue(result)

    def __sub__(self, other):
        """ Удаляет из текущего значение переданный список стран.
        :param other список 2-х буквенных кодов стран:
        :return:

        """
        if isinstance(other, (list, tuple)):
            other = countries_to_bin(other)
        result = [0, 0, 0, 0]
        for i in xrange(4):
            result[i] = self.binaries[i] & ~other[i]
        return CountriesValue(result)

    def __contains__(self, item):
        """ Проверяет вхождение страны в список.
        :param item: 2-х символьный код страны для проверки
        :return: True/False

        """
        binaries = countries_to_bin([item])
        for i in xrange(4):
            if binaries[i]:
                return bool(self.binaries[i] & binaries[i])
        return False


class CountriesFieldDescriptor(Creator):
    """ Управляет доступом к значениям битовых полей.
    """
    def __get__(self, obj, objtype=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return CountriesValue([getattr(obj, f)
                               for f in self.field.bit_field_names])

    def __set__(self, obj, value):
        if isinstance(value, (list, tuple)):
            value = countries_to_bin(value)
        elif isinstance(value, CountriesValue):
            value = value.binaries
        value = zip(self.field.bit_field_names, list(value))
        for f_name, binary in value:
            setattr(obj, f_name, binary)


class CountriesField(models.Field):
    """ Класс поля для хранения битовой карты стран.
    """
    def contribute_to_class(self, cls, name):
        """ Создаёт битовые поля, регистрирует себя как виртуальное поле,
        регистриует дескриптор.

        """
        self.name = name
        self.cls = cls
        self.bit_field_names = []

        for i in range(0, 4):
            bit_field_name = "_{}_b{}".format(name, i)
            start = i * MAX_FLAG_COUNT
            end = i * MAX_FLAG_COUNT + MAX_FLAG_COUNT
            flags = alpha2_index[start:end]
            bit_field = BitField(flags=flags, default=0, editable=False)
            cls.add_to_class(bit_field_name, bit_field)
            self.bit_field_names.append(bit_field_name)

        cls._meta.add_virtual_field(self)
        setattr(cls, name, CountriesFieldDescriptor(self))

        models.signals.pre_init.connect(self.instance_pre_init, sender=cls,
                                        weak=False)

    def instance_pre_init(self, signal, sender, args, kwargs, **opts):
        """ Обработка создания объекта модели.
        """
        if self.name in kwargs:
            countries = kwargs.pop(self.name)
            binaries = countries_to_bin(countries)
            kwargs.update(dict(zip(self.bit_field_names, binaries)))
