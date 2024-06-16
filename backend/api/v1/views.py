from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from store.models import Category

from .serializers import CategorySerializer

User = get_user_model()


class CategoryView(ListAPIView):
    """View вывода списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
