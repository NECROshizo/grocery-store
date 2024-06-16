from rest_framework import serializers

from store.models import Category, Product, SubCategory


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

    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'subcategories',
            'image',
        )


class ShortCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий без подкатегорий"""

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'image',
        )


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов"""

    category = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'slug',
            'category',
            'subcategory',
            'images',
        )

    def get_category(self, obj: Product) -> dict:
        return ShortCategorySerializer(obj.subcategory.category).data

    def get_images(self, obj: Product) -> dict:
        absolute_url = self.context.get('request').build_absolute_uri
        return [
            absolute_url(obj.original_image.url),
            absolute_url(obj.medium_image.url),
            absolute_url(obj.small_image.url),
        ]
