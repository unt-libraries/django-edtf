from django.conf.urls import patterns, url
from edtf.views import urlerror, edtf_form, boolean_result, result_json
from django.conf import settings

urlpatterns = patterns(

    # global prefix
    '',

    # this is the view for the standard user input form landing page
    url(r'^$', edtf_form, name='edtf_form'),

    # this view is a plain-text lowercase boolean result: true/false
    # we removed this view as it is not necessary
    # i'd like to keep it commented for my own reference as i learn django
    # - Joey
    # url(r'^isValid$', boolean_result, name='boolean_result'),

    # this view is a json representation of the result
    url(r'^isValid.json$', result_json, name='results_json'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^.*$', urlerror),
    )
