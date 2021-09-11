from django.urls import include, path
from rest_framework import routers
from .views import *



urlpatterns = [
	path('', index, name="home"),
	path('busreg', bookseat, name="busreg"),
	path('breakjourney',graphjourney,name="breakjourney")
]
