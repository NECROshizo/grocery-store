from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum, F
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from store.models import Category, Product, ShoppingCart

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ShoppingCartInputSerializer,
    ShoppingCartSerializer,
    ShoppingCartSummarySerializer,
)

User = get_user_model()


class CategoryView(ListAPIView):
    """Вывод списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ListAPIView):
    """Вывод списка товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartView(ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView):
    """Представление для работы с корзиной товаров."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingCart.objects.filter(user=user)

    def _validate_and_serialize_products(self, request):
        products = request.data.get('products', [])
        if not products:
            raise ValidationError({'detail': "Список продуктов должен содержаться в 'products'"})

        serializer = ShoppingCartInputSerializer(data=products, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def list(self, request, *args, **kwargs):
        """Метод для получения списка продуктов в корзине с суммарной информацией."""
        response = super().list(request, *args, **kwargs)
        user = request.user
        user_cart = ShoppingCart.objects.filter(user=user).prefetch_related('product')
        summary = user_cart.aggregate(
            total_items=Sum('count'),
            total_price=Sum(F('count') * F('product__price')),
        )
        response.data = {'product': response.data, 'summary': ShoppingCartSummarySerializer(summary).data}
        return response

    def post(self, request, *args, **kwargs):
        """Метод для добавления продуктов в корзину."""
        validated_data = self._validate_and_serialize_products(request)
        user = request.user

        with transaction.atomic():
            for item in validated_data:
                product = item['product']
                count = item['count']
                cart_item, created = ShoppingCart.objects.get_or_create(user=user, product=product)
                if created:
                    cart_item.count = count
                else:
                    cart_item.count += count
                cart_item.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Метод для обновления количества продуктов в корзине."""
        validated_data = self._validate_and_serialize_products(request)
        user = request.user

        with transaction.atomic():
            for item in validated_data:
                product = item['product']
                count = item['count']
                cart_item, _ = ShoppingCart.objects.get_or_create(user=user, product=product)
                cart_item.count = count
                cart_item.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Метод для удаления продуктов из корзины."""
        validated_data = self._validate_and_serialize_products(request)
        user = request.user

        with transaction.atomic():
            for item in validated_data:
                product = item['product']
                count = item['count']
                cart_item = ShoppingCart.objects.filter(user=user, product=product).first()
                if cart_item:
                    if cart_item.count <= count:
                        cart_item.delete()
                    else:
                        cart_item.count -= count
                        cart_item.save()
        return Response({'result': 'success'}, status=status.HTTP_204_NO_CONTENT)


class ShoppingCartClearView(DestroyAPIView):
    """Представление полной очистки корзины."""

    queryset = ShoppingCart.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        return self.queryset.filter(user=user)
