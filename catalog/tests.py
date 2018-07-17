from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
#from catalog.models import Category, Product, Phablet, Parfum
from django.utils import timezone
from selenium import webdriver
from catalog.views import index
# Create your tests here.


class HomePageTest(TestCase):
    """
    """

    def test_root_url(self):
        """
        This Testcase uses resolve to test if the user
        can get to the home page.
        resolve return a ResolverMatch object.
        """
        root_url = resolve('/')
        self.assertEqual(root_url.func, index)
        

    def test_home_is_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>',html)
        self.assertTrue(html.endswith('</html>'))

        