from rest_framework import serializers

from store.models import Category, Product, ShoppingCart, SubCategory


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
        request = self.context.get('request')
        if request:
            absolute_url = request.build_absolute_uri
            return [
                absolute_url(obj.original_image.url),
                absolute_url(obj.medium_image.url),
                absolute_url(obj.small_image.url),
            ]
        return [obj.original_image.url, obj.medium_image.url, obj.small_image.url]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор продуктовой корзины"""

    product = serializers.SerializerMethodField()

    # product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'count',
        )

    def get_product(self, obj: ShoppingCart) -> dict:
        return ProductSerializer(obj.product).data


class ShoppingCartSummarySerializer(serializers.ModelSerializer):
    """Сериализатор сводной информации по продуктовой корзине"""

    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = ShoppingCart
        fields = (
            'total_items',
            'total_price',
        )


class ShoppingCartInputSerializer(serializers.Serializer):
    """Сериализатор для взаимодействия продуктов в корзине"""

    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='slug')
    count = serializers.IntegerField(min_value=1)

    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'count',
        )
