from functools import wraps


def jsonp(f):
    """Wrap a json response in a callback, and set the mimetype (Content-Type)
    header accordinglly (will wrap in text/javascript if there is a callback).
    If the "callback" or "jsonp" parameters are provided, will wrap the json
    output in callback({thejson})

    Usage:

    @jsonp
    def my_json_view(request):
        d = { 'key': 'value' }
        return HTTPResponse(json.dumps(d), content_type='application/json')
    """
    @wraps(f)
    def jsonp_wrapper(request, *args, **kwargs):
        resp = f(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp
        if 'callback' in request.GET:
            callback = request.GET['callback']
            resp['Content-Type'] = 'application/javascript; charset=utf-8'
            resp.content = "%s(%s)" % (callback, resp.content)
            return resp
        else:
            return resp

    return jsonp_wrapper
