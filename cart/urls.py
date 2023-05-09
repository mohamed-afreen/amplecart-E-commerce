from django.urls import path, include
from . import views
urlpatterns = [

    path('cart', views.cart, name="cart"),
    path('addTocart/<int:id>', views.addTocart, name="addTocart"),
    path('removecart/<int:id>', views.removecart, name="removecart"),
    path('checkout', views.checkout, name="checkout"),
    path('paywith_wallet', views.paywith_wallet, name="paywith_wallet"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('addToWatchlist', views.addToWatchlist, name="addToWatchlist"),
    path('removeFromWatchlist', views.removeFromWatchlist,
         name="removeFromWatchlist"),
    path('removeWatchlist/<int:id>', views.removeWatchlist, name="removeWatchlist"),
]
