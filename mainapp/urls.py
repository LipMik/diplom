from django.urls import path
from .views import (BaseView,
                    ProductDetailView,
                    CategoryDetailView,
                    CartView,
                    AddProduct,
                    DeleteFromCartView,
                    ChangeQTY,
                    SortView
    )


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    # products/ct_model/product_slug/
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # endpoint for Catergories
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    # CartView
    path('cart/', CartView.as_view(), name='cart'),
    # # AddProduct
    path('add_product/<str:ct_model>/<str:slug>/', AddProduct.as_view(), name='add_product'),
    # DeleteFromCartView
    path('remove-product/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    # ChangeQTY
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTY.as_view(), name='change_qty'),
    # Checkout
    path('sort/', SortView.as_view(), name='sort')
]


