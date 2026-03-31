"""
URL configuration for the Product Catalog project.

Routes:
    /admin/  — Django admin panel
    /        — Product listing page
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]
