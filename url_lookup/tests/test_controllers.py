from django.test import TestCase
from url_lookup.controllers import URLInfo
from url_lookup.models import URLBlacklist


class URLInfoTestCase(TestCase):
    model = URLBlacklist
    fixtures = ['URLBlacklist.json']

    def test_get_info(self):
        is_url_exists = URLInfo.get_info(URLInfo(), 'example.com')
        self.assertTrue(is_url_exists)
        is_exists = URLInfo.get_info(URLInfo(), 'google.com')
        self.assertFalse(is_exists)
