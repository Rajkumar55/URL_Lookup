import json
from rest_framework import status
from rest_framework.test import APITestCase


class URLLookupTestCase(APITestCase):
    fixtures = ['URLBlacklist.json']

    def test_url_info_with_malicious_url(self):
        response = self.client.get('/urlinfo/1/example.com:80/show')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'malicious')
        self.assertEqual(url_info['host_name'], 'example.com')
        self.assertIsInstance(url_info['port'], int)
        self.assertEqual(url_info['port'], 80)
        self.assertEqual(url_info['path'], 'show')

    def test_url_info_with_safe_url(self):
        response = self.client.get('/urlinfo/1/google.com:443/show')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'safe')
        self.assertEqual(url_info['port'], 443)
        self.assertEqual(url_info['path'], 'show')

    def test_list_urls(self):
        response = self.client.get('/urlinfo/url/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'success')

    def test_add_url_with_valid_data(self):
        mock_data = {
            'url': 'example.ru'
        }
        response = self.client.post('/urlinfo/url/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'success')
        self.assertEqual(url_info['message'], 'Inserted successfully')

    def test_add_url_with_invalid_data(self):
        mock_data = {
            'url': ''
        }
        response = self.client.post('/urlinfo/url/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'error')

    def test_update_url_with_valid_data(self):
        mock_data = {
            "url_id": 1,
            "url": "example.net"
        }
        response = self.client.put('/urlinfo/url/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'success')
        self.assertEqual(url_info['message'], 'Updated successfully')

    def test_update_url_with_invalid_data(self):
        mock_data = {
            "url_id": 5,
            "url": "example.net"
        }
        response = self.client.put('/urlinfo/url/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url_info = json.loads(response.content)
        self.assertEqual(url_info['status'], 'error')
