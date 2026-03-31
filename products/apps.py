"""App configuration for the products application."""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration class for the products Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
