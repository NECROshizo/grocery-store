from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

User = get_user_model()


class BaseCategory(models.Model):
    title = models.CharField(_('Название'), help_text=_('Введите название категории'), unique=True, max_length=200)

    slug = models.SlugField(
        _('Слаг'),
        help_text=_('Используйте slug состаящий из латинских букв, цифр и символа _'),
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=_('Используйте slug состаящий из латинских букв, цифр и символа _'),
            )
        ],
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # my_string = self.title.translate(
            #     str.maketrans(
            #         "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            #         "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            #     ))
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(BaseCategory):
    image = models.ImageField(
        _('Категория'),
        upload_to='categories/',
        db_comment=_('Изображение категории'),
        help_text=_('Выберете изображение категории'),
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        db_table_comment = _('Категории')


class SubCategory(BaseCategory):
    image = models.ImageField(
        _('Подкатегория'),
        upload_to='subcategories/',
        db_comment=_('Изображение подкатегории'),
        help_text=_('Выберете изображение подкатегории'),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name=_('Категория'),
        help_text=_('Введите родительскую категорию'),
        db_comment=_('Категория'),
    )

    class Meta:
        verbose_name = _('Подкатегория')
        verbose_name_plural = _('Подкатегории')
        db_table_comment = _('Подкатегории')


class Product(models.Model):
    title = models.CharField(
        _('Название'),
        help_text=_('Введите название продукта'),
        db_comment=_('Название'),
        unique=True,
        blank=False,
        max_length=200,
    )

    price = models.DecimalField(
        _('Цена'),
        help_text=_('Введите цену продукта'),
        db_comment=_('Цена'),
        decimal_places=2,
        max_digits=13,
        null=False,
        validators=[MinValueValidator(0)],
        error_messages={
            'min_value': _('Минимальная цена должна быть больше или равна 0'),
        },
    )

    slug = models.SlugField(
        _('Слаг'),
        help_text=_('Используйте slug состаящий из латинских букв, цифр и символа _'),
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message=_('Используйте slug состаящий из латинских букв, цифр и символа _'),
            )
        ],
        unique=True,
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Подкатегория продукта'),
        help_text=_('Выберете подкатегорию продукта'),
        db_comment=_('Подкатегория продукта'),
    )

    original_image = models.ImageField(
        _('Продукт'),
        upload_to='products/',
        db_comment=_('Оригинальное изображение продукта'),
        help_text=_('Выберете оригинальное изображение продукта'),
    )

    medium_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 60},
    )

    small_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60},
    )

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        db_table_comment = _('Продукты')

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_cart',
        verbose_name=_('Пользователь'),
        help_text=_('Выберите пользователя, добавившего продукт в корзину.'),
        db_comment=_('Пользователь'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shoping_cart',
        verbose_name=_('Продукт'),
        help_text=_('Выберите продукт, добавленный в корзину.'),
    )

    count = models.PositiveIntegerField(
        _('Количесво продуктов'),
        help_text=_('Выберите количество продуктов, добавленных в корзину.'),
        db_comment=_('Количество продуктов'),
        validators=[MinValueValidator(1)],
        error_messages={
            'min_value': _('Минимальное количество продуктов должно быть больше или равно 1'),
        },
        default=1,
        blank=False,
        null=False,
    )

    added_at = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
        help_text=_('Дата и время добавления товара в корзину.'),
        db_comment=_('Дата добавления'),
    )

    class Meta:
        verbose_name = _('Корзина с продуктами')
        verbose_name_plural = _('Корзины с продуктами')
        db_table_comment = _('Продукты')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_shoping_card',
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.product} : {self.count}'
