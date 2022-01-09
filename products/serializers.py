from rest_framework import serializers
from products.models import *


# All serializers for method GET

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductsDetailSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    class Meta:
        model = Product
        fields = ['id','name','url_image','price','discount','category']
