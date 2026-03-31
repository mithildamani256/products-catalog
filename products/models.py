"""
Models for the Product Catalog application.

Defines three core models:
    Category — groups products into logical sections
    Tag      — flexible labels that can be applied to many products
    Product  — the main entity with price, description, category, and tags
"""

from django.db import models


class Category(models.Model):
    """
    Represents a top-level product category (e.g. Electronics, Clothing).

    Fields:
        name        — unique display name for the category
        description — optional longer description
        created_at  — timestamp set automatically on creation
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    A short label that can be attached to many products (e.g. Sale, New).

    Fields:
        name       — unique tag label
        created_at — timestamp set automatically on creation
    """

    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The core product entity in the catalog.

    Fields:
        name        — product display name
        description — full product description
        price       — decimal price up to 99,999,999.99
        category    — FK to Category; deletes products if category is removed
        tags        — M2M to Tag; optional labels
        created_at  — timestamp set automatically on creation
        updated_at  — timestamp updated automatically on every save
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # so basically many products belong to one category
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
    )

    # Every product can have zero or more tags
    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
