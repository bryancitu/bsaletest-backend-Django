from django.urls import path
from products.views import *
from django.conf.urls import url

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category'),
    path('products/<category>/', ProductByCategoryView.as_view(), name='product_category'),
    path('product-detail/<name>/', ProductsDetailView.as_view(), name='product_detail'),
    path('search/<product>/', ProductSearch.as_view(), name='product_search'),
]
