from django.shortcuts import render

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *
import re

# Create your views here.

class CategoryView(ListAPIView):
    serializer_class = CategorySerializers

    def get_queryset(self):
        category_show = Category.objects.all()
        return category_show

class ProductByCategoryView(ListAPIView):
    serializer_class = ProductsDetailSerializers

    def get_queryset(self):
        cat = self.kwargs['category']
        products_show = Product.objects.filter(category__name=cat)
        return products_show

class ProductsDetailView(ListAPIView):
    serializer_class = ProductsDetailSerializers

    def get_queryset(self):
        product = self.kwargs['name']
        products_show = Product.objects.filter(name=product)
        return products_show



# --------------------------------- PAGINATION -----------------------------------
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

# --------------------------------------------------------------------------------

class ProductSearch(ListAPIView):
    serializer_class = ProductsDetailSerializers
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        product = self.kwargs['product']

        if product != 'None':
            products = Product.objects.filter(name__icontains=product)
            return products
        
        return Product.objects.all()