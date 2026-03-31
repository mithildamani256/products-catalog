"""
Tests for the Product Catalog application.
"""

from django.test import TestCase, Client
from django.urls import reverse

from .models import Category, Tag, Product


class ModelTests(TestCase):
    """Test to ensure that the models are created correctly and that relationships work."""

    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.tag = Tag.objects.create(name='New')
        self.product = Product.objects.create(
            name='Wireless Headphones',
            description='Noise cancelling headphones.',
            price='99.99',
            category=self.category,
        )
        self.product.tags.add(self.tag)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'New')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Wireless Headphones')

    def test_product_has_category(self):
        self.assertEqual(self.product.category.name, 'Electronics')

    def test_product_has_tag(self):
        self.assertIn(self.tag, self.product.tags.all())


class ProductListViewTests(TestCase):
    """Test the product_list view — response, search, category, and tag filtering."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('product_list')

        # Categories
        self.electronics = Category.objects.create(name='Electronics')
        self.clothing = Category.objects.create(name='Clothing')

        # Tags
        self.tag_new = Tag.objects.create(name='New')
        self.tag_sale = Tag.objects.create(name='Sale')

        # Products
        self.p1 = Product.objects.create(
            name='Wireless Headphones',
            description='Noise cancelling headphones.',
            price='99.99',
            category=self.electronics,
        )
        self.p1.tags.add(self.tag_new)

        self.p2 = Product.objects.create(
            name='USB-C Cable',
            description='Durable charging cable.',
            price='12.99',
            category=self.electronics,
        )
        self.p2.tags.add(self.tag_sale)

        self.p3 = Product.objects.create(
            name='Cotton T-Shirt',
            description='Comfortable organic cotton shirt.',
            price='19.99',
            category=self.clothing,
        )
        self.p3.tags.add(self.tag_new, self.tag_sale)

    # Basic response

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_all_products_shown_by_default(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['result_count'], 3)

    # Search

    def test_search_matches_name(self):
        response = self.client.get(self.url, {'search': 'headphones'})
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p1, response.context['products'])

    def test_search_matches_description(self):
        response = self.client.get(self.url, {'search': 'charging cable'})
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p2, response.context['products'])

    def test_search_is_case_insensitive(self):
        response = self.client.get(self.url, {'search': 'COTTON'})
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p3, response.context['products'])

    def test_search_no_match_returns_empty(self):
        response = self.client.get(self.url, {'search': 'nonexistent'})
        self.assertEqual(response.context['result_count'], 0)

    # Category filter

    def test_filter_by_category(self):
        response = self.client.get(self.url, {'category': self.electronics.id})
        self.assertEqual(response.context['result_count'], 2)
        self.assertNotIn(self.p3, response.context['products'])

    def test_invalid_category_returns_all(self):
        # A non-numeric category value should be ignored and basically return all products
        response = self.client.get(self.url, {'category': 'abc'})
        self.assertEqual(response.context['result_count'], 3)

    # Tag filter

    def test_filter_by_single_tag(self):
        response = self.client.get(self.url, {'tags': self.tag_new.id})
        # p1 and p3 both have the 'New' tag
        self.assertEqual(response.context['result_count'], 2)
        self.assertNotIn(self.p2, response.context['products'])

    def test_filter_by_multiple_tags_is_and_logic(self):
        # Only p3 has both 'New' AND 'Sale'
        response = self.client.get(self.url, {
            'tags': [self.tag_new.id, self.tag_sale.id]
        })
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p3, response.context['products'])

    def test_multiple_tags_no_duplicate_products(self):
        # p3 has two matching tags but it must appear exactly once
        response = self.client.get(self.url, {
            'tags': [self.tag_new.id, self.tag_sale.id]
        })
        products = list(response.context['products'])
        self.assertEqual(products.count(self.p3), 1)

    # ------------------------------------------------------------------
    # Combined filters
    # ------------------------------------------------------------------

    def test_search_and_category_combined(self):
        response = self.client.get(self.url, {
            'search': 'cable',
            'category': self.electronics.id,
        })
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p2, response.context['products'])

    def test_category_and_tag_combined(self):
        # Electronics + Sale tag is only in p2
        response = self.client.get(self.url, {
            'category': self.electronics.id,
            'tags': self.tag_sale.id,
        })
        self.assertEqual(response.context['result_count'], 1)
        self.assertIn(self.p2, response.context['products'])
