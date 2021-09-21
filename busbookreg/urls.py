from django.urls import include, path
from rest_framework import routers
from .views import *
from time import sleep

urlpatterns = [
	path('', index, name="home"),
	path('busreg/<str:username>', Bookseat.as_view(username="Tiasha"), name="busreg"),
	path('breakjourney/<str:username>/<str:stations>',graphjourney,name="breakjourney")
]
