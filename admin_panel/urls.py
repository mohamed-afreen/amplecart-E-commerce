from django.urls import path
from . import views


urlpatterns = [
    path("", views.admin_login, name='admin_login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('user_list', views.user_list, name='user_list'),
    path('block_user/<id>/', views.block_user, name="block_user"),
    path('unblock_user/<id>/', views.unblock_user, name="unblock_user"),
    path('wallet_details', views.wallet_details, name='wallet_details'),
]
