import json
from unittest import expectedFailure

from django.core.urlresolvers import reverse, resolve
from django.test import SimpleTestCase, RequestFactory

from edtf.views import edtf_form, boolean_result, urlerror, result_json


class TestURLs(SimpleTestCase):

    def test_edtf_form_url(self):
        view = resolve(reverse('edtf:edtf_form')).func
        self.assertEqual(view, edtf_form)

    def test_results_json_url(self):
        view = resolve(reverse('edtf:results_json')).func
        self.assertEqual(view, result_json)


class TestEdtfFormView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        request = self.factory.get('/')
        response = edtf_form(request)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        url = reverse('edtf:edtf_form')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edtf/edtf_form.html')


class TestBooleanResultView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        request = self.factory.get('/', {'date': '', 'level': ''})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 200)

    def test_returns_400_without_date(self):
        request = self.factory.get('/', {'level': '1'})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 400)

    # The view should return an HTTP 400 response when no level is present.
    @expectedFailure
    def test_returns_400_without_level(self):
        request = self.factory.get('/', {'date': 'March 3rd, 2016'})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 400)

    def test_returns_true_with_valid_date(self):
        request = self.factory.get('/', {'date': '2012-06-12', 'level': '0'})
        response = boolean_result(request)
        self.assertHTMLEqual(response.content, 'true')

    def test_returns_false_with_invalid_date(self):
        request = self.factory.get('/', {'date': 'March 3rd, 2016', 'level': '2'})
        response = boolean_result(request)
        self.assertHTMLEqual(response.content, 'false')


class TestResultJsonView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': ''})
        self.assertEqual(response.status_code, 200)

    def test_returns_true_with_valid_date(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013?-12-12'})
        self.assertEqual(json.loads(response.content), {'validEDTF': True})

    def test_returns_false_with_invalid_date(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013-23-????'})
        self.assertEqual(json.loads(response.content), {'validEDTF': False})

    def test_returns_400_without_date(self):
        request = self.factory.get('/', {'level': '1'})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)

    # The view should return an HTTP 400 response when no level is present.
    @expectedFailure
    def test_returns_400_without_level(self):
        request = self.factory.get('/', {'date': 'March 3rd, 2016', 'level': ''})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)
