from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase



class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('customuser-list')
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
