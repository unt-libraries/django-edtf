import json
import pytest

from django.urls import resolve, reverse
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

    def test_returns_400_without_date(self):
        request = self.factory.get('/', {'level': '1'})
        response = result_json(request)
        self.assertEqual(response.status_code, 400)

    def test_correct_template_used(self):
        url = reverse('edtf:edtf_form')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edtf/edtf_form.html')


class TestResultJsonView:

    def setUp(self):
        self.factory = RequestFactory()

    @pytest.mark.parametrize('date',
                             [
                                 ('2013?-12-12'),
                                 ('2012'),
                                 ('2013/2014'),
                             ])
    def test_return_200(self, date, client):
        response = client.get(reverse('edtf:results_json'), {'date': date})
        assert response.status_code == 200

    @pytest.mark.parametrize('date, levelFeature',
                             [
                                 ('2013', '3'),
                                 ('2015/2018', ''),
                                 ('', '0'),
                             ])
    def test_return_400_for_levelFeature(self, date, levelFeature, client):
        response = client.get(reverse('edtf:results_json'), {'date': date,
                                                             'levelFeature': levelFeature})
        assert response.status_code == 400

    @pytest.mark.parametrize('date, levelConforms',
                             [
                                 ('2013', '4'),
                                 ('2015/2018', ''),
                                 ('', '0'),
                             ])
    def test_return_400_for_levelConforms(self, date, levelConforms, client):
        response = client.get(reverse('edtf:results_json'), {'date': date,
                                                             'levelConforms': levelConforms})
        assert response.status_code == 400

    @pytest.mark.parametrize('input_date, edtf_output',
                             [
                                 ('2013?-12-12', True),
                                 ('2019-12/%2020', True),
                                 ('2013-23-????', False),
                                 ('0000/-0001', False),
                             ])
    def test_edtf_date(self, input_date, edtf_output, client):
        response = client.get(reverse('edtf:results_json'), {'date': input_date})
        assert json.loads(response.content) == {'validEDTF': edtf_output}

    @pytest.mark.parametrize('input_date, levelConforms, edtf_output',
                             [
                                 ('2013?-12-12', '2', True),
                                 ('-1995/2000', '2', True),
                                 ('../1985-04-12', '2', True),
                                 ('?2004-06~-10/2004-06-%11', '2', True),
                                 ('1111-01-01/1111', '1', True),
                                 ('1985-04-XX', '1', True),
                                 ('1990', '0', True),
                                 ('2013-23-????', '2', False),
                                 ('-0000', '2', False),
                                 ('2004-06-11%/2004-06~', '2', False),
                                 ('15XX-12-25', '1', False),
                                 ('1863- 03-29', '1', False),
                                 (None, '0', False),
                                 ('Y170000002', '0', False),
                             ])
    def test_date_and_levelConforms(self, input_date, levelConforms, edtf_output, client):
        response = client.get(reverse('edtf:results_json'), {'date': input_date,
                                                             'levelConforms': levelConforms})
        assert json.loads(response.content) == {'validEDTF': edtf_output}

    @pytest.mark.parametrize('input_date, levelFeature, edtf_output',
                             [
                                 ('2013?-12-12', '2', True),
                                 ('-1995/2000', '1', True),
                                 ('1111-01-01/1111', '0', True),
                                 ('../1985-04-12', '1', True),
                                 ('?2004-06~-10/2004-06-%11', '2', True),
                                 ('2013-23-????', '2', False),
                                 ('2012-10-10T10:50:10Z15', '2', False),
                                 ('0000', '2', False),
                                 ('15XX-12-25', '1', False),
                                 ('0000/0000', 1, False),
                                 ('1863- 03-29', '0', False),
                                 (None, '0', False),
                                 ('Y170000002', '0', False),
                             ])
    def test_date_and_levelFeature(self, input_date, levelFeature, edtf_output, client):
        response = client.get(reverse('edtf:results_json'), {'date': input_date,
                                                             'levelFeature': levelFeature})
        assert json.loads(response.content) == {'validEDTF': edtf_output}
