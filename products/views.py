"""
Views for the Product Catalog application.
"""

from django.shortcuts import render
from django.db.models import Q

from .models import Product, Category, Tag


def product_list(request):
    """
    Display a filterable, searchable list of all products.

    Supported GET parameters:
        search   (str)       — case-insensitive substring match on product name/description
        category (str)       — Category primary key to filter by
        tags     (list[str]) — one or more Tag primary keys; all must match (AND)
    """

    # Join category and prefetch tags up-front to avoid N+1 queries in the template
    products = Product.objects.select_related('category').prefetch_related('tags')

    categories = Category.objects.order_by('name')
    tags = Tag.objects.order_by('name')

    # Search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Category filter — just a guard against non-numeric input before hitting the ORM
    category_id = request.GET.get('category', '').strip()
    if category_id.isdigit():
        products = products.filter(category_id=category_id)
    else:
        category_id = ''

    # Tags filter - sanitize first and then basically chain one .filter() per tag so that
    # selecting two tags returns products that have BOTH (AND logic).
    # A final .distinct() prevents duplicate rows caused by the M2M joins.
    selected_tags = [int(t) for t in request.GET.getlist('tags') if t.isdigit()]
    for tag_id in selected_tags:
        products = products.filter(tags__id=tag_id)
    if selected_tags:
        products = products.distinct()

    product_list_evaluated = list(products)

    # Annotate each category so the template avoids a string == comparison
    for cat in categories:
        cat.is_selected = (str(cat.id) == category_id)

    context = {
        'products': product_list_evaluated,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'selected_tags': selected_tags,
        'result_count': len(product_list_evaluated),
    }

    return render(request, 'products/product_list.html', context)
