from django.test import TestCase
import pytest
from  .views import infun, login, outfun
from forms import *
from django.urls import reverse

# Create your tests here.

class Falserequest_for_get:
    def __init__(self,name_of_url,method_of_url):
        self.requests=name_of_url
        self.method=method_of_url
        self.META={"CSRF_COOKIE":"1234trtyfyugyg23"}

class Falserequest_for_post:
    def __init__(self,name_of_url):
        self.requests=name_of_url
        self.method="POST"
        self.META={"CSRF_COOKIE":"1234trtyfyugyg23"}
        self.POST={"data":{"your_name":1234,"your_email":"train","your_password":"0986"}}

def test_login():
    get_check=Falserequest_for_get("/check/login","GET")
    checked_log_get=login(get_check)
    print(checked_log_get)
    post_check=Falserequest_for_post("check/login")
    checked_log_post=login(post_check)
    #doubt: post_check is a dictionary whose key is "data" . but after sending post_check into the login
    #function it is giving error after doing request.post["data"]

def test_inbus():
    req=Falserequest_for_get("/check/inbus","GET")
    print(infun(req,"testing_name"))

def test_outbus():
    req=Falserequest_for_get("/check/outbus","GET")
    print(outfun(req,"testing_name"))


    


    
