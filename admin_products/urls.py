from django.urls import path, include
from . import views
urlpatterns = [

    path('admin_products', views.admin_products, name="admin_products"),
    path('edit_product/<int:id>/', views.edit_product, name="edit_product"),
    path('delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('add_product', views.add_product, name="add_product"),
    path('soldout_products', views.soldout_products, name="soldout_products"),

]
