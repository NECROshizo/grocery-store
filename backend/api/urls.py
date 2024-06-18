from django.urls import include, path, re_path

app_name = 'api'

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
