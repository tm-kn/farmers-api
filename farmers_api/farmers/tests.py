from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Farmer
from .views import FarmerViewSet


class FarmerMoTest(TestCase):

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


class FarmersAPITest(APITestCase):

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            'john', 'john@example.com', 'somepassword')

        self.superuser_token = Token.objects.create(user=self.superuser)

        self.data = [
            Farmer(first_name='John', surname='Smith', town='Harrogate'),
            Farmer(first_name='Tom', surname='Darcy', town='London'),
        ]

        Farmer.objects.bulk_create(self.data)

    def test_can_get_farmers_list(self):
        response = self.client.get(reverse('farmer-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_farmers_list(self):
        response = self.client.get(reverse('farmer-list'), format='json')

        [self.assertContains(response, x)
         for x in ['John', 'Tom', 'London', 'Harrogate']]

    def test_can_get_farmer_detail(self):
        random_farmer = Farmer.objects.order_by('?').first()
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_farmer_detail(self):
        random_farmer = Farmer.objects.order_by('?')[0]
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        response = self.client.get(url, format='json')

        [self.assertContains(response, x) for x in [
            random_farmer.first_name, random_farmer.surname,
            random_farmer.town, random_farmer.pk]]

    def test_guest_cannot_delete_farmer(self):
        random_farmer = Farmer.objects.order_by('?')[0]
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_delete_farmer(self):
        random_farmer = Farmer.objects.order_by('?')[0]
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        self._authenticate_superuser()

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_guest_cannot_update_farmer(self):
        random_farmer = Farmer.objects.order_by('?')[0]
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        response = self.client.patch(url, data={'first_name': 'Updated name'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_update_farmer(self):
        random_farmer = Farmer.objects.order_by('?')[0]
        url = reverse('farmer-detail', kwargs=dict(pk=random_farmer.pk))

        self._authenticate_superuser()

        response = self.client.patch(url, data={'first_name': 'Updated name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if data has been updated in database
        random_farmer.refresh_from_db()
        self.assertEqual(random_farmer.first_name, 'Updated name')

    def test_guest_cannot_create_farmer(self):
        response = self.client.post(
            reverse('farmer-list'),
            data={'first_name': 'Test', 'surname': 'Test2', 'town': 'TestTown'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_create_farmer(self):
        data = {'first_name': 'Test', 'surname': 'Test2', 'town': 'TestTown'}

        self._authenticate_superuser()

        response = self.client.post(reverse('farmer-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if data has been added to database
        self.assertTrue(Farmer.objects.filter(**data).exists())

    def _authenticate_superuser(self):
        self.client.force_authenticate(
            user=self.superuser, token=self.superuser_token)
