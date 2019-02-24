from django.urls import reverse
from django.test import TestCase


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = reverse('lists:home')
        self.assertEqual(found, '/')
