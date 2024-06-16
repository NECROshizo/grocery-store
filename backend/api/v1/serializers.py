from rest_framework import serializers

from store.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегорий"""

    class Meta:
        model = SubCategory
        fields = (
            'title',
            'slug',
            'image',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    subcategories = SubCategorySerializer(
        many=True,
    )

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'subcategories',
            'image',
        )
