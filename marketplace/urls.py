from django.urls import path
from . import views

urlpatterns = [
    path('',views.market , name='market'),
    path('product/<slug:slug>',views.product , name='product'),
    path('newproduct',views.add_product , name='add_product'),
    path('filter',views.filter , name='filter'),
    path('search',views.search , name='search'),
    path('myproducts',views.myproducts , name='myproducts'),
    path('editproduct/<slug:slug>/',views.edit_product , name='edit_product'),
    path('delete_product/<slug:slug>',views.delete_product , name='delete_product'),
]