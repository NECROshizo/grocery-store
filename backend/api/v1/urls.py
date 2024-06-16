from django.urls import path

from backend.api.v1.views import CategoryView

app_name = 'v1'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
]
