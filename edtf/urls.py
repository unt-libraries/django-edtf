from django.conf.urls import url
from edtf.views import edtf_form, result_json

app_name = 'edtf'
urlpatterns = [
    url(r'^$', edtf_form, name='edtf_form'),
    url(r'^isValid.json$', result_json, name='results_json'),
]
