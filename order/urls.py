from django.urls import path
from . import views


urlpatterns = [
    path('place_order/',view=views.place_order,name='place_order'),
    path('payment/',view=views.payment,name='payment'),
]
