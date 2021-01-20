from django.urls import path
from edtf.views import edtf_form, result_json

app_name = 'edtf'
urlpatterns = [
    path('', edtf_form, name='edtf_form'),
    path('isValid.json', result_json, name='results_json'),
]
