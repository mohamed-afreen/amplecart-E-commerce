from django.urls import path
from . import views

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.logout, name='logout'),
    path('number_otp_verify', views.number_otp_verify, name='number_otp_verify'),
    path('otp_resend/<str:new_phone_number>',
         views.otp_resend, name="otp_resend"),
    path('products/', views.products, name="products"),
    path('product_details/<int:id>/',
         views.product_details, name="product_details"),
    path('my_profile', views.my_profile, name="my_profile"),
    path('edit_profile/<int:id>', views.edit_profile, name="edit_profile"),
    path('my_products', views.my_products, name="my_products"),
    path('edit_my_product/<int:id>/',
         views.edit_my_product, name="edit_my_product"),
    path('product_dont_Sell/<int:id>/',
         views.product_dont_Sell, name="product_dont_Sell"),
    path('product_resell/<int:id>/', views.product_resell, name="product_resell"),
    path('changePassword/<int:id>', views.changePassword, name="changePassword"),
    path('categoryview/<str:category_name>',
         views.categoryview, name="categoryview"),
    path('wallet', views.wallet, name='wallet'),
    path('withdraw_wallet', views.withdraw_wallet, name='withdraw_wallet'),
    # path('remove_wallet', views.remove_wallet, name='remove_wallet'),
    path('invoice_generate/<int:id>',
         views.invoice_generate, name="invoice_generate"),
    path('terms_and_conditions', views.terms_and_conditions,
         name="terms_and_conditions")
]
