from django.urls import path

from backend.api.v1.views import CategoryView, ProductView

app_name = 'v1'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
    path('products/', ProductView.as_view(), name='products'),
]
