from django.shortcuts import redirect, render
from datetime import datetime


# Create your views here.

def infun(request):
    checkin= datetime.now()
    print(f"checkin time : {checkin}")
    checkin_time=checkin.strftime("%H:%M:%S")
    checkin_month=checkin.month
    checkin_day=checkin.day
    print(f"checkin time : {checkin_time} checkin month and day : {checkin_month}  {checkin_day} ")
    return redirect("/")

def outfun(request):
    checkout= datetime.now()
    print(f"checkin time : {checkout}")
    checkout_time=checkout.strftime("%H:%M:%S")
    checkout_month=checkout.month
    checkout_day=checkout.day
    print(f"checkout time : {checkout_time} checkout month and day : {checkout_month}  {checkout_day} ")
    return redirect("/")
