import json

from django.core.urlresolvers import reverse, resolve
from django.test import SimpleTestCase, RequestFactory

from edtf.views import edtf_form, result_json


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


class TestResultJsonView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2012'})
        self.assertEqual(response.status_code, 200)

    def test_returns_true_with_valid_date_no_level(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013?-12-12'})
        self.assertEqual(json.loads(response.content), {'validEDTF': True})

    def test_returns_true_with_valid_date_and_level(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013-12-12',
                                                                  'level': '0'})
        self.assertEqual(json.loads(response.content), {'validEDTF': True})

    def test_returns_400_with_valid_date_and_invalid_level(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013', 'level': '3'})
        self.assertEqual(response.status_code, 400)

    def test_returns_400_with_valid_date_and_empty_level(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013', 'level': ''})
        self.assertEqual(response.status_code, 400)

    def test_returns_false_with_invalid_date(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': '2013-23-????'})
        self.assertEqual(json.loads(response.content), {'validEDTF': False})

    def test_returns_400_without_date(self):
        request = self.factory.get('/', {'level': '1'})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_with_empty_date(self):
        request = self.factory.get('/', {'date': ''})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)
