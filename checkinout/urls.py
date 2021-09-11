from django.urls import path
from .views import *

urlpatterns = [
    path('inbus/<str:n>',infun,name="inbus"),
    path("outbus/<str:n>",outfun,name="outbus"),
    path("register", registration, name="register"),
    path("login", login, name="login"),
]