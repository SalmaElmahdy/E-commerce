from django.urls import path

from . import views


urlpatterns = [
    path('',views.cart,name='cart'),
    path('add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('remove_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
]
