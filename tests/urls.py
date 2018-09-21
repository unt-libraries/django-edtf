from django.conf.urls import include, url

urlpatterns = [
    url(r'^edtf/', include('edtf.urls', namespace='edtf'))
]
