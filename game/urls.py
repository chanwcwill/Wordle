from django.urls import path
from . import views

urlpatterns = [
    path('', views.wordle_game, name='wordle_game'),
] 