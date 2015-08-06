"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
try:
    # the json module was included in the stdlib in python 2.6
    # http://docs.python.org/library/json.html
    import json
except ImportError:
    # simplejson 2.0.9 is available for python 2.4+
    # http://pypi.python.org/pypi/simplejson/2.0.9
    # simplejson 1.7.3 is available for python 2.3+
    # http://pypi.python.org/pypi/simplejson/1.7.3
    import simplejson as json
from django.utils import unittest
from ExtendedDateTimeFormat import valid_edtf
from edtf.views import edtf_form, boolean_result, urlerror, result_json
from django.test import Client

class ViewsTest(unittest.TestCase):
    """
    This test class makes sure views get called and return proper response codes

    """

    def setUp(self):
        """every test needs a client"""
        self.c = Client()

    def test_json(self):
        """test json view and responses"""
        # issue get request to test
        good_response = self.c.get('/edtf/isValid.json?date=3113')
        not_found_response = self.c.get('/edtf/isValid.jso?date=3113')
        bad_response = self.c.get('/edtf/isValid.json?year=3113')
        # check that the response is 200 OK.
        self.assertEqual(good_response.status_code, 200)
        self.assertEqual(not_found_response.status_code, 404)
        self.assertEqual(bad_response.status_code, 400)

    def test_boolean_result(self):
        """test boolean result view and responses"""
        # issue get request to test
        good_response = self.c.get('/edtf/isValid.json?date=2000')
        bad_response = self.c.get('/edtf/isVald.json?dat=2000')
        # check that the response is 200 OK.
        self.assertEqual(good_response.status_code, 200)
        self.assertTrue(json.loads(good_response.content)['validEDTF'])
        self.assertEqual(bad_response.status_code, 404)

    def test_edtf_form(self):
        """test edtf form view and response"""
        # issue get request to test
        response = self.c.get('/edtf/')
        # check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


class DatesTest(unittest.TestCase):
    """This class does testing on the validation of dates"""

    def test_basic_dates(self):
        """Test the output of basic dates"""
        # cycle through 0000-9999 and assert true
        for i in range(0000, 9999):
            self.assertTrue(valid_edtf.is_valid(str(i).zfill(4)))

    def test_blatant_errors(self):
        self.assertFalse(valid_edtf.is_valid("open/open"))

    def test_level_0_validity(self):
        '''
        tests the examples given in the spec:
        http://www.loc.gov/standards/datetime/pre-submission.html#level0
        '''
        # date
        self.assertTrue(valid_edtf.isLevel0("2001-02-03"))
        self.assertTrue(valid_edtf.isLevel0("2008-12"))
        self.assertTrue(valid_edtf.isLevel0("2008"))
        self.assertTrue(valid_edtf.isLevel0("-0999"))
        self.assertTrue(valid_edtf.isLevel0("0000"))
        # date and time
        self.assertTrue(valid_edtf.isLevel0("2001-02-03T09:30:01"))
        self.assertTrue(valid_edtf.isLevel0("2004-01-01T10:10:10Z"))
        self.assertTrue(valid_edtf.isLevel0("2004-01-01T10:10:10+05:00"))
        # interval
        self.assertTrue(valid_edtf.isLevel0("1964/2008"))
        self.assertTrue(valid_edtf.isLevel0("2004-06/2006-08"))
        self.assertTrue(valid_edtf.isLevel0("2004-02-01/2005-02-08"))
        self.assertTrue(valid_edtf.isLevel0("2004-02-01/2005-02"))
        self.assertTrue(valid_edtf.isLevel0("2004-02-01/2005"))
        self.assertTrue(valid_edtf.isLevel0("2005/2006-02"))
        self.assertTrue(valid_edtf.isLevel0("2005/2006-02"))

    def test_level_1_validity(self):
        '''
        tests the examples given in the spec:
        http://www.loc.gov/standards/datetime/pre-submission.html#level1
        '''
        # uncertain
        self.assertTrue(valid_edtf.isLevel1("1984?"))
        self.assertTrue(valid_edtf.isLevel1("2004-06?"))
        self.assertTrue(valid_edtf.isLevel1("2004-06-11?"))
        self.assertTrue(valid_edtf.isLevel1("1984~"))
        self.assertTrue(valid_edtf.isLevel1("1984?~"))
        # unspecified
        self.assertTrue(valid_edtf.isLevel1("199u"))
        self.assertTrue(valid_edtf.isLevel1("19uu"))
        self.assertTrue(valid_edtf.isLevel1("1999-uu"))
        self.assertTrue(valid_edtf.isLevel1("1999-01-uu"))
        self.assertTrue(valid_edtf.isLevel1("1999-uu-uu"))
        # extended interval
        self.assertTrue(valid_edtf.isLevel1("2004-06-01/unknown"))
        self.assertTrue(valid_edtf.isLevel1("2004-01-01/open"))
        self.assertTrue(valid_edtf.isLevel1("1984~/2004-06"))
        self.assertTrue(valid_edtf.isLevel1("1984/2004-06~"))
        self.assertTrue(valid_edtf.isLevel1("1984?/2004?~"))
        # year exceeding 4 digits
        self.assertTrue(valid_edtf.isLevel1("y170000002"))
        self.assertTrue(valid_edtf.isLevel1("y-170000002"))
        # season. ex: spring, 2012
        self.assertTrue(valid_edtf.isLevel1("2012-21"))

    def test_level_2_validity(self):
        '''
        tests the examples given in the spec:
        http://www.loc.gov/standards/datetime/pre-submission.html#level2
        '''
        # partial, uncertain/approximate
        self.assertTrue(valid_edtf.isLevel2('2004?-06-11'))
        self.assertTrue(valid_edtf.isLevel2('2004-06~-11'))
        self.assertTrue(valid_edtf.isLevel2('2004-(06)?-11'))
        self.assertTrue(valid_edtf.isLevel2('2004-06-(11)~'))
        self.assertTrue(valid_edtf.isLevel2('2004-(06)?~'))
        self.assertTrue(valid_edtf.isLevel2('2004-(06-11)?'))
        self.assertTrue(valid_edtf.isLevel2('2004?-06-(11)~'))
        self.assertTrue(valid_edtf.isLevel2('(2004-(06)~)?'))
        self.assertTrue(valid_edtf.isLevel2('2004?-(06)?~'))
        self.assertTrue(valid_edtf.isLevel2('(2004)?-06-04~'))
        self.assertTrue(valid_edtf.isLevel2('(2011)-06-04~'))
        self.assertTrue(valid_edtf.isLevel2('2011-(06-04)~'))
        self.assertTrue(valid_edtf.isLevel2('2011-23~'))
        # partial unspecified
        self.assertTrue(valid_edtf.isLevel2('156u-12-25'))
        self.assertTrue(valid_edtf.isLevel2('15uu-12-25'))
        self.assertTrue(valid_edtf.isLevel2('15uu-12-uu'))
        self.assertTrue(valid_edtf.isLevel2('1560-uu-25'))
        # one of a set
        self.assertTrue(valid_edtf.isLevel2('[1667,1668, 1670..1672]'))
        self.assertTrue(valid_edtf.isLevel2('[..1760-12-03]'))
        self.assertTrue(valid_edtf.isLevel2('[1760-12..]'))
        self.assertTrue(valid_edtf.isLevel2('[1760-01, 1760-02, 1760-12..]'))
        self.assertTrue(valid_edtf.isLevel2('[1667, 1760-12]'))
        # multiple dates
        self.assertTrue(valid_edtf.isLevel2('{1667,1668, 1670..1672}'))
        self.assertTrue(valid_edtf.isLevel2('{1960, 1961-12}'))
        # masked precision
        self.assertTrue(valid_edtf.isLevel2('196x'))
        self.assertTrue(valid_edtf.isLevel2('19xx'))
        # extended interval
        self.assertTrue(valid_edtf.isLevel2('2004-06-(01)~/2004-06-(20)~'))
        self.assertTrue(valid_edtf.isLevel2('2004-06-uu/2004-07-03'))
        # year exceeding 4 digits exponential form
        self.assertTrue(valid_edtf.isLevel2('y17e7'))
        self.assertTrue(valid_edtf.isLevel2('y-17e7'))
        self.assertTrue(valid_edtf.isLevel2('y17101e4p3'))
        # season qualified
        self.assertTrue(valid_edtf.isLevel2('2001-21^southernHemisphere'))

    def test_random_is_valid_false_checks(self):
        '''
        non-level based validity checks
        '''
        self.assertFalse(valid_edtf.is_valid("2012/20uu"))
        self.assertFalse(valid_edtf.is_valid("y00000022"))
        self.assertFalse(valid_edtf.is_valid("2014/2000"))
        self.assertFalse(valid_edtf.is_valid("123"))
        self.assertFalse(valid_edtf.is_valid("2012-12-12T12:12:12ZZ"))
        self.assertFalse(valid_edtf.is_valid("20127"))
        self.assertFalse(valid_edtf.is_valid("2012\2013"))
