from typing import Any

from django.contrib import admin
from django.db.models import QuerySet
from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeText

from .models import Category, Product, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'show_subcategory', 'show_preview')
    search_fields = (
        'title',
        'slug',
    )
    ordering = ('title', 'slug')
    list_per_page = 20
    inlines = [SubCategoryInline]

    @admin.display(description='Превью категории')
    def show_preview(self, obj: Category) -> SafeText:
        images_column = format_html('<img src="{}" style="max-height: 100px;">', obj.image.url)
        return images_column

    @admin.display(description='Подкатегории')
    def show_subcategory(self, obj: Category) -> SafeText:
        subcategory_column = format_html_join(
            ', ', '<span>{}</span>', ((sub_cat.title,) for sub_cat in obj.subcategories.all())
        )
        return subcategory_column

    def get_search_results(self, request, queryset, search_term) -> tuple[QuerySet | Any, bool]:
        queryset, have_duplicates = super().get_search_results(request, queryset, search_term)
        if search_term:
            subcategory_queryset = SubCategory.objects.filter(title=search_term)
            category_ids = subcategory_queryset.values_list('category_id', flat=True)
            queryset |= self.model.objects.filter(id__in=category_ids)
        return queryset, have_duplicates


@admin.register(SubCategory)
class SubCategoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_category', 'slug', 'show_preview')
    search_fields = ('title', 'slug', 'category__title')
    list_filter = ('category__title',)
    ordering = ('title', 'slug')
    list_per_page = 20

    @admin.display(description='Превью подкатегории')
    def show_preview(self, obj: SubCategory) -> SafeText:
        images_column = format_html('<img src="{}" style="max-height: 100px;">', obj.image.url)
        return images_column

    @admin.display(description='Категория')
    def show_category(self, obj: SubCategory) -> str:
        return obj.category.title


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'show_category', 'show_subcategory', 'show_preview')
    search_fields = ('title',)
    # list_filter = ("username", "email",)
    ordering = ('title',)
    list_per_page = 20

    @admin.display(description='Подкатегория')
    def show_subcategory(self, obj: Product) -> str:
        return obj.subcategory.title

    @admin.display(description='Категория')
    def show_category(self, obj: Product) -> str:
        return obj.subcategory.category.title

    @admin.display(description='Превью подкатегории')
    def show_preview(self, obj: SubCategory) -> SafeText:
        images_column = format_html('<img src="{}" style="max-height: 100px;">', obj.original_image.url)
        return images_column
