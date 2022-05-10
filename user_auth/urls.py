from django.contrib import admin
from django.urls import path, include
from user_auth import views
import user_auth 
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('page', views.page, name='page'),
    path('dashboard', views.dashboard, name='dashboard'),

]