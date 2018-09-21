from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
from django.conf import settings
from edtf_validate import valid_edtf
from edtf.decorators import jsonp


def edtf_form(request):
    """Renders the edtf form landing page to the user"""

    return render(
        request,
        'edtf/edtf_form.html',
        {
            'maintenance_message': settings.MAINTENANCE_MSG,
        },
    )


@jsonp
def result_json(request):
    """Returns boolean result of valid_edtf.py script in json format"""

    # grab the date from the request argument
    date = request.GET.get('date')
    jsonedtfdict = {}
    if date is '' or date is None:
        return HttpResponseBadRequest()
    elif 'level' in request.GET:
        level = request.GET.get('level')
        if level is '' or level is None or int(level) > 2 or int(level) < 0:
            return HttpResponseBadRequest()
        # build dictionary to serialize to json
        funcs = {
            '0': valid_edtf.isLevel0(date),
            '1': valid_edtf.isLevel1(date),
            '2': valid_edtf.isLevel2(date),
        }
        jsonedtfdict = {
            'validEDTF': valid_edtf.is_valid(date) and funcs[level]
        }
    else:
        # build dictionary to serialize to json
        jsonedtfdict = {
            'validEDTF': valid_edtf.is_valid(date)
        }

    # dump the dict to as an HttpResponse
    response = HttpResponse(content_type='application/json; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'X-Requested-With'
    json.dump(
        jsonedtfdict,
        fp=response,
        indent=4,
        sort_keys=True,
        ensure_ascii=False,
    )
    return response
