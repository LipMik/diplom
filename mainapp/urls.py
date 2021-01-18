from django.urls import path
from .views import test_view, ProductDetailView


urlpatterns = [
    path('', test_view, name='base'),
    # products/ct_model/product_slug/
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail')
]

