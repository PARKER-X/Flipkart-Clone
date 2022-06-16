from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('book/', views.Books, name='book'),
    path('cloth/', views.Cloths, name='cloth'),
    path('food/', views.Foods, name='food'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')
]