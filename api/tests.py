from django.db.models import Q
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json

from .models import Vps
from .serializers import VpsSerializer

client = Client()


class GetSingleVpsTest(TestCase):
    """ Test module for GET single VPS """

    def setUp(self):
        self.small_vps = Vps.objects.create(
            cpu_cores=4, ram=8, hdd=500, status='started')
        self.medium_vps = Vps.objects.create(
            cpu_cores=8, ram=16, hdd=1000, status='stopped')
        self.large_vps = Vps.objects.create(
            cpu_cores=16, ram=32, hdd=1500, status='blocked')

    def test_get_valid_single_puppy(self):
        response = client.get(reverse('api:retrieve_vps', kwargs={'vps_id': self.small_vps.pk}))
        large_vps = Vps.objects.get(pk=self.small_vps.pk)
        serializer = VpsSerializer(large_vps)
        self.assertEqual(response.data['vps'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('api:retrieve_vps', kwargs={'vps_id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateVpsTest(TestCase):
    """ Test module for creating VPS """

    def setUp(self):
        self.valid_payload = {
            'cpu_cores': 8,
            'ram': 32,
            'hdd': 1000,
            'status': 'started'
        }
        self.invalid_payload = {
            'cpu_cores': 0,
            'ram': 123,
            'hdd': 500,
            'status': 'blocked'
        }

    def test_create_valid_vps(self):
        # print(json.dumps(self.valid_payload))
        response = client.post(
            reverse('api:create_vps'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_vps(self):
        response = client.post(
            reverse('api:create_vps'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetFilteredVpsTest(TestCase):
    """ Test module for GET filtered VPS """

    def setUp(self):
        self.small_vps = Vps.objects.create(
            cpu_cores=8, ram=8, hdd=500, status='started')
        self.medium_vps = Vps.objects.create(
            cpu_cores=12, ram=32, hdd=2000, status='stopped')
        self.large_vps = Vps.objects.create(
            cpu_cores=32, ram=64, hdd=2500, status='blocked')

    def test_get_valid_filtered_vps(self):
        response = client.get(f'https://127.0.0.1:8000/api/get_vps/?cpu_cores={self.small_vps.cpu_cores}&ram={self.large_vps.ram}')
        large_vps = Vps.objects.filter(Q(cpu_cores=self.small_vps.cpu_cores) | Q(ram=self.large_vps.ram))
        serializer = VpsSerializer(large_vps, many=True)
        self.assertEqual(response.data['vps'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_filtered_vps(self):
        response = client.get('https://127.0.0.1:8000/api/get_vps/?cpu_cores=1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChangeVpsStatusTest(TestCase):
    """ Test module for changing status of VPS """

    def setUp(self):
        self.valid_payload = {
            'cpu_cores': 8,
            'ram': 32,
            'hdd': 1000,
            'status': 'started'
        }
        self.invalid_payload = {
            'cpu_cores': 0,
            'ram': 123,
            'hdd': 500,
            'status': 'blocked'
        }

    def test_valid_change_status_vps(self):
        # print(json.dumps(self.valid_payload))
        response = client.post(
            reverse('api:change_vps_status'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_change_status_vps(self):
        response = client.post(
            reverse('api:change_vps_status'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)