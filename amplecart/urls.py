from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path('defi_the_game', views.defi_the_game, name='defi_the_game'),
    path('art_blocks', views.art_blocks, name='art_blocks'),
    path('blogs', views.blogs, name='blogs'),
]
