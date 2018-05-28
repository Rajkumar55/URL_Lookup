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
