"""
Management command: populate_sample_data

Wipes all the currently existing catalog data and inserts a curated set of sample
categories, tags, and products so the application is demo ready
straight after migration.

Usage:
    python manage.py populate_sample_data
"""

from django.core.management.base import BaseCommand

from products.models import Category, Tag, Product


class Command(BaseCommand):
    """Populate the database with sample catalog data."""

    help = 'Clear existing data and populate the database with sample products.'

    def handle(self, *args, **options):
        """Execute the command: clear then re-seed all catalog data."""

        # 1. Wipe existing data
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

        # 2. Create Categories
        category_data = [
            ('Electronics', 'Electronic devices and gadgets'),
            ('Clothing', 'Apparel and fashion items'),
            ('Home & Garden', 'Home decor and garden supplies'),
            ('Sports', 'Sports equipment and accessories'),
            ('Books', 'Books and reading materials'),
        ]

        categories = {}
        for name, description in category_data:
            cat = Category.objects.create(name=name, description=description)
            categories[name] = cat
            self.stdout.write(f'Created category: {name}')

        # ------------------------------------------------------------------ #
        # 3. Create Tags                                                        #
        # ------------------------------------------------------------------ #
        tag_names = [
            'New', 'Sale', 'Popular', 'Eco-friendly', 'Premium',
            'Budget-Friendly', 'Limited Stock', 'Best Seller',
            'Trending', 'Recommended',
        ]

        tags = {}
        for name in tag_names:
            tag = Tag.objects.create(name=name)
            tags[name] = tag
            self.stdout.write(f'Created tag: {name}')

        # 4. Create Products
        products_data = [
            # --- Electronics ---
            (
                'Wireless Bluetooth Headphones',
                'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
                '129.99',
                'Electronics',
                ['New', 'Popular', 'Premium'],
            ),
            (
                'USB-C Charging Cable',
                '6ft durable USB-C charging cable compatible with all modern devices.',
                '12.99',
                'Electronics',
                ['Budget-Friendly', 'Best Seller'],
            ),
            (
                'Smartphone Screen Protector',
                'Tempered glass screen protector with bubble-free installation.',
                '9.99',
                'Electronics',
                ['Sale', 'Popular', 'Budget-Friendly'],
            ),
            (
                'Wireless Mouse',
                'Ergonomic wireless mouse with precision tracking and 18-month battery.',
                '24.99',
                'Electronics',
                ['Trending', 'Premium'],
            ),
            (
                'Portable Phone Charger',
                '20000mAh portable battery with fast charging support.',
                '35.99',
                'Electronics',
                ['Popular', 'New', 'Recommended'],
            ),
            # --- Clothing ---
            (
                'Cotton T-Shirt',
                '100% organic cotton comfortable t-shirt in multiple colors.',
                '19.99',
                'Clothing',
                ['Eco-friendly', 'Budget-Friendly'],
            ),
            (
                'Winter Jacket',
                'Insulated winter jacket with waterproof outer layer.',
                '89.99',
                'Clothing',
                ['Premium', 'Popular'],
            ),
            (
                'Athletic Running Shoes',
                'Lightweight running shoes with gel cushioning and breathable mesh.',
                '119.99',
                'Clothing',
                ['New', 'Trending', 'Popular'],
            ),
            (
                'Denim Jeans',
                'Classic blue denim jeans with comfortable fit.',
                '49.99',
                'Clothing',
                ['Best Seller', 'Budget-Friendly'],
            ),
            (
                'Wool Beanie',
                'Warm wool knit beanie perfect for winter.',
                '29.99',
                'Clothing',
                ['Sale', 'Recommended'],
            ),
            # --- Home & Garden ---
            (
                'Bamboo Plant Stand',
                'Eco-friendly bamboo plant stand for indoor plants.',
                '39.99',
                'Home & Garden',
                ['Eco-friendly', 'Trending'],
            ),
            (
                'LED Desk Lamp',
                'Energy-efficient LED desk lamp with adjustable brightness.',
                '34.99',
                'Home & Garden',
                ['Eco-friendly', 'Popular', 'Budget-Friendly'],
            ),
            (
                'Throw Pillow Set',
                'Set of 4 decorative throw pillows with various patterns.',
                '59.99',
                'Home & Garden',
                ['New', 'Popular'],
            ),
            (
                'Kitchen Organizer Set',
                'Set of storage containers to organize your kitchen.',
                '44.99',
                'Home & Garden',
                ['Budget-Friendly', 'Trending'],
            ),
            (
                'Wall Art Canvas',
                'Beautiful canvas wall art in modern designs.',
                '79.99',
                'Home & Garden',
                ['Premium', 'Recommended'],
            ),
            # --- Sports ---
            (
                'Professional Soccer Ball',
                'Official size 5 soccer ball for professional play.',
                '54.99',
                'Sports',
                ['Premium', 'Popular'],
            ),
            (
                'Yoga Mat',
                'Non-slip yoga mat with carrying strap and cushioning.',
                '34.99',
                'Sports',
                ['Budget-Friendly', 'Best Seller'],
            ),
            (
                'Dumbbells Set',
                'Set of adjustable dumbbells for home gym workouts.',
                '149.99',
                'Sports',
                ['Premium', 'New', 'Trending'],
            ),
            (
                'Tennis Racket',
                'Professional grade tennis racket with graphite frame.',
                '89.99',
                'Sports',
                ['Premium', 'Popular'],
            ),
            (
                'Basketball',
                'Official size basketball for indoor and outdoor play.',
                '29.99',
                'Sports',
                ['Budget-Friendly', 'Recommended', 'Sale'],
            ),
            # --- Books ---
            (
                'Python Programming Guide',
                'Comprehensive guide to learning Python programming from basics to advanced.',
                '39.99',
                'Books',
                ['Popular', 'Recommended'],
            ),
        ]

        for name, description, price, category_name, tag_names_list in products_data:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=categories[category_name],
            )
            # Attach tags via M2M
            for tag_name in tag_names_list:
                product.tags.add(tags[tag_name])

            self.stdout.write(f'Created product: {name}')

        self.stdout.write(self.style.SUCCESS(
            '\n✓ Successfully populated database with sample data!'
        ))
