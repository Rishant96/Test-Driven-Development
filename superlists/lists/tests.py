from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import lists.views as lists_views


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = reverse('lists:home')
        self.assertEqual(found, '/')

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = lists_views.home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(response.content.decode(), expected_html)
