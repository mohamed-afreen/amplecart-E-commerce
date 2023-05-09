from django.urls import path
from . import views
urlpatterns = [

    path('category', views.category, name="category"),
    path('delete_category/<int:id>/',
         views.delete_category, name="delete_category"),
    path('add_category', views.add_category, name="add_category"),

]
