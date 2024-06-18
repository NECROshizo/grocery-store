from django.urls import path

from api.v1.views import CategoryView, ProductView, ShoppingCartView, ShoppingCartClearView

app_name = 'v1'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
    path('products/', ProductView.as_view(), name='products'),
    path('shopping-cart/', ShoppingCartView.as_view(), name='shopping-cart'),
    path('shopping-cart/clear', ShoppingCartClearView.as_view(), name='shopping-cart-clear'),
]
