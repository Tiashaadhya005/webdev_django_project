from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.http import HttpResponseRedirect
from .forms import NameForm
from utils import *


def authenticate(user_email,password):
    my_db=get_db()
    my_collection=get_coll_for_user_acc()
    is_there=my_collection.find_one({"useremail":user_email,"user_password":password})
    if is_there:
        return True
    return False

def registration(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        p=form.data
        if form.is_valid():
            my_db=get_db()
            my_collection=get_coll_for_user_acc()
            my_collection.insert_one({"username":p['your_name'],"useremail":p['your_email'],"user_mobile":p['your_mobile'],"user_password":p['your_password']})
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("not valid")
    else:
        form = NameForm()
        return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        p=form.data
        if form.is_valid():
            if authenticate(p['your_email'],p['your_password']):
                return render(request,"index.html",{'header_mssg':f"Hi {p['your_name']}"})
            return HttpResponseRedirect('/')
        else:
            a=form.errors
            print(a)
            login_again="<h3>something is wrong <a href='/check/login'>try again</a></h3>"
            return HttpResponse(login_again)
    else:
        form = NameForm()
        return render(request, 'login.html', {'form': form})
    

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
