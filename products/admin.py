"""
Admin configuration for the Product Catalog application.

Registers Category, Tag, and Product with customized list views,
search fields, and filters to make the admin panel productive.
"""

from django.contrib import admin

from .models import Category, Tag, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for product categories."""

    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin view for product tags."""

    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin view for products with filtering and M2M tag widget."""

    list_display = ['name', 'category', 'price', 'created_at']
    list_filter = ['category', 'tags', 'created_at']
    search_fields = ['name', 'description']
    # Render the M2M tag relationship as a horizontal select widget
    filter_horizontal = ['tags']
