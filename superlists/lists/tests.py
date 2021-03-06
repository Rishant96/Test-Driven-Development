from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import lists.views as lists_views
from lists.models import Item


def clean_html_of_csrf_for_local_comparison(html_data):
    """Removes content that is omitted by render_to_string(),
       for fair comparison between the response and local html.

       Expects that each logical line also occupies one physical line.
       (Especially the lines to be cleaned.)"""
    lines = html_data.split('\n')
    for line in lines:
        if 'name="csrfmiddlewaretoken"' in line:
            lines[lines.index(line)] = ''
    return '\n'.join(lines)


def trim_each_line_in_string(data):
    lines = data.split('\n')
    for line in lines:
        lines[lines.index(line)] = line.strip()
    return '\n'.join(lines)


def prepare_response_and_local_html_for_comparison(response_data, html_data):
    cleaned_html = clean_html_of_csrf_for_local_comparison(response_data)

    response_data, html_data = trim_each_line_in_string(cleaned_html),\
        trim_each_line_in_string(html_data)

    return response_data, html_data


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = reverse('lists:home')
        # changing the assertion from '/' to '/lists/' for now
        self.assertEqual(found, '/lists/')

    def test_local_clean_method_for_csrf_tokens(self):
        raw_html = """
            <html>
              <head>
                <title>Sample csrf token</title>
              </head>
              <body>
                  <input type="hidden"  name="csrfmiddlewaretoken" value="x"/>
              </body>
            </html>
        """

        expected_html = """
            <html>
              <head>
                <title>Sample csrf token</title>
              </head>
              <body>

              </body>
            </html>
        """

        cleaned_html = clean_html_of_csrf_for_local_comparison(raw_html)
        self.assertEqual(cleaned_html, expected_html,
                         'CSRF token not cleaned properly.')

    def test_string_trimmer(self):
        test_str = """
            hello,   
            ouoeu, 
            auoenthu,
                oeuoeu,  
            oeu,
        """

        expected_str = """
            hello,
            ouoeu,
            auoenthu,
            oeuoeu,
            oeu,
        """

        trimmed_str = trim_each_line_in_string(test_str)
        self.assertEqual(trimmed_str, trim_each_line_in_string(expected_str),
                         'Not Trimming properly, trim output:' + trimmed_str)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = lists_views.home_page(request)
        expected_html = render_to_string('lists/home.html')
        cleaned_html = clean_html_of_csrf_for_local_comparison(response.content
                                                               .decode())
        cleaned_html, expected_html \
            = prepare_response_and_local_html_for_comparison(
              response.content.decode(), expected_html)
        self.assertEqual(cleaned_html, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_next'] = 'A new list item'

        lists_views.home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_next'] = 'A new list item'

        response = lists_views.home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the'
                         '-world')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        lists_views.home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = lists_views.home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    """
    A class to test the list view.
    """
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
