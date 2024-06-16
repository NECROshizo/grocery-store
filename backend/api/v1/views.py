from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from store.models import Category, Product

from .serializers import CategorySerializer, ProductSerializer

User = get_user_model()


class CategoryView(ListAPIView):
    """Вывод списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ListAPIView):
    """Вывод списка товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
