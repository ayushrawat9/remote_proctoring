## urls.py
from django.urls import path
from game.views import *


urlpatterns = [
    path('', index),
    path('play/<room_code>', game),
]