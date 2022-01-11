from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'url_image', 'price', 'discount', 'category']
    list_filter = ['category']
    list_editable = ['price']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)