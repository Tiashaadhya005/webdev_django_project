from django.urls import path
from .views import *

urlpatterns = [
    path('inbus',infun,name="inbus"),
    path("outbus",outfun,name="outbus"),
    path("register", registration, name="register"),
    path("login", login, name="login"),
]