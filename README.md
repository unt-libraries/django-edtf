Django-edtf
===========


About
-----

Django-edtf is an app which provides the service of validating dates that comply with the
Extended Date Time Format ([Levels 0-2](http://www.loc.gov/standards/datetime/pre-submission.html)).
The simple interface may be used from the browser or from the command-line, using a utility
such as `curl`. The response returned will usually be an HTTP 200 with a JSON object
containing `{ "validEDTF": true }` or `{ "validEDTF": false }`. In some circumstances (no date value
entered or an invalid level value) you may receive an HTTP 400 to indicate that something is invalid.


Requirements
------------

* Django >= 1.8
* Python >= 2.7
* [edtf-validate](https://github.com/unt-libraries/edtf-validate) >= 1.0.0


Installation
------------

1. Download and install from source code.

```console
$ pip install git+git://github.com/unt-libraries/django-edtf.git
```

2. Add app to INSTALLED_APPS.

```python
INSTALLED_APPS = (
    'edtf',
)
```

3. Include the URLs.

```python
urlpatterns = [
    url(r'^edtf/', include('edtf.urls', namespace='edtf')),
]
```

4. Add the MAINTENANCE_MSG var in the settings.

```python
MAINTENANCE_MSG = ''
```

License
-------

See LICENSE
