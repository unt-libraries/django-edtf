from django.urls import include, path

urlpatterns = [
    path('edtf/', include('edtf.urls', namespace='edtf'))
]
