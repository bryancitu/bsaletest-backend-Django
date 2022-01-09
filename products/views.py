from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *

# Create your views here.

class CategoryView(ListAPIView):
    serializer_class = CategorySerializers

    def get_queryset(self):
        category_show = Category.objects.all()
        print(category_show)
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
