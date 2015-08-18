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

    def test_view_returns_200(self):
        request = self.factory.get('/')
        response = edtf_form(request)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        url = reverse('edtf:edtf_form')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edtf/edtf_form.html')

    def test_validates_compliant_extended_date_time(self):
        pass

    def test_does_not_validate_non_compliant_extended_date_time(self):
        pass


class TestBooleanResultView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        request = self.factory.get('/', {'date': '', 'level': ''})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 200)

    def test_returns_400_without_date(self):
        level = '1'
        request = self.factory.get('/', {'level': level})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 400)

    # The view should return an HTTP 400 response when no level is present.
    @expectedFailure
    def test_returns_400_without_level(self):
        date = 'March 3rd, 2016'
        request = self.factory.get('/', {'date': date})
        response = boolean_result(request)
        self.assertEqual(response.status_code, 400)

    def test_returns_true_with_valid_date(self):
        date = '2012-06-12'
        level = '0'
        request = self.factory.get('/', {'date': date, 'level': level})
        response = boolean_result(request)
        self.assertHTMLEqual(response.content, 'true')

    def test_returns_false_with_invalid_date(self):
        date = 'March 3rd, 2016'
        level = '2'
        request = self.factory.get('/', {'date': date, 'level': level})
        response = boolean_result(request)
        self.assertHTMLEqual(response.content, 'false')


class TestResultJsonView(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200(self):
        response = self.client.get(reverse('edtf:results_json'), {'date': ''})
        self.assertEqual(response.status_code, 200)

    def test_returns_true_with_valid_date(self):
        date = '2013?-12-12'
        response = self.client.get(reverse('edtf:results_json'), {'date': date})
        self.assertEqual(json.loads(response.content), {'validEDTF': True})

    def test_returns_false_with_invalid_date(self):
        date = '2013-23-????'
        response = self.client.get(reverse('edtf:results_json'), {'date': date})
        self.assertEqual(json.loads(response.content), {'validEDTF': False})

    def test_returns_400_without_date(self):
        level = '1'
        request = self.factory.get('/', {'level': level})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)

    # The view should return an HTTP 400 response when no level is present.
    @expectedFailure
    def test_returns_400_without_level(self):
        date = 'March 3rd, 2016'
        request = self.factory.get('/', {'date': date, 'level': ''})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)
