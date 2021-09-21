from django.test import TestCase
import pytest
from .views import *

# Create your tests here.

class Falserequest_for_get:
    def __init__(self,name_of_url):
        self.requests=name_of_url
        self.method="GET"
        self.META={"CSRF_COOKIE":"1234trtyfyugyg23"}

class Falserequest_for_post:
    def __init__(self,name_of_url,start,end):
        self.requests=name_of_url
        self.method="POST"
        self.META={"CSRF_COOKIE":"1234trtyfyugyg23"}
        self.POST={"data":{"your_name":1234,"your_email":"train","your_password":"0986"}}
        self.data={"StartingLocation":start,"EndLocation":end}

def test_bookseat():
    req_for_get=Falserequest_for_get("/busreg")
    checked_get=Bookseat.as_view(),{"request":req_for_get,"username":"weather"}
    print(checked_get)
    req_for_post=Falserequest_for_post("/busreg","ENVIROment","POLLUTED")
    checked_post=Bookseat.as_view()
    print(checked_post)
