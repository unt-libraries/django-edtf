from django.conf.urls import patterns, url
from edtf.views import edtf_form, result_json

urlpatterns = patterns(
    '',
    url(r'^$', edtf_form, name='edtf_form'),
    url(r'^isValid.json$', result_json, name='results_json'),
)
