from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Farmer


class FarmerModelTest(TestCase):

    def test_string_representation(self):
        farmer = Farmer(first_name='John', surname='Smith', town='Harrogate')

        self.assertEqual(str(farmer), '%s %s' %
                         (farmer.first_name, farmer.surname))

    def test_verbose_name(self):
        self.assertEqual(Farmer._meta.verbose_name, 'farmer')

    def test_verbose_plural_name(self):
        self.assertEqual(Farmer._meta.verbose_name_plural, 'farmers')

    def test_getting_full_name(self):
        farmer = Farmer(first_name='Tom Doggo',
                        surname='Pupper', town='Harrogate')

        self.assertEqual(farmer.get_full_name(), 'Tom Doggo Pupper')

    def test_getting_short_name(self):
        farmer = Farmer(first_name='Tom Doggo',
                        surname='Pupper', town='Harrogate')

        self.assertEqual(farmer.get_short_name(), 'T. Pupper')

    def test_fail_if_surname_is_not_supplied(self):
        farmer = Farmer(first_name='Tom', town='Leeds')
        with self.assertRaises(ValidationError):
            farmer.full_clean()

    def test_fail_if_first_name_is_not_supplied(self):
        farmer = Farmer(surname='Pupper', town='Harrogate')
        with self.assertRaises(ValidationError):
            farmer.full_clean()

    def test_fail_if_town_is_not_supplied(self):
        farmer = Farmer(first_name='Test', surname='Family Name')
        with self.assertRaises(ValidationError):
            farmer.full_clean()
