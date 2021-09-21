from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required,permission_required
import pytest
from forms import NameForm
from utils import *


def auth_enticate(user_email,password):
    #this function will authenticate/check if the user exists or not and will return 
    #a boolean accordingly.

    #my_db will store the db name
    my_db=get_db() 
    #my_collection will store the collection name
    my_collection=get_coll_for_user_acc()
    is_there=my_collection.find_one({"useremail":user_email,"user_password":password})
    if is_there:
        return True
    return False

def registration(request):
    #this function will register user and store the data into mongodb database
    if request.method == 'POST':
        form = NameForm(request.POST)
        p=form.data
        #if the form data is valid
        if form.is_valid():
            my_db=get_db()
            my_collection=get_coll_for_user_acc()
            #store the details of user into mongodb collection
            my_collection.insert_one(
                {"username":p['your_name'],"useremail":p['your_email'],"user_mobile":p['your_mobile'],"user_password":p['your_password']}
                )
            # after storing it will redirect to main page
            return render(request,"index.html",{'header_mssg':f"{p['your_name']}"})
        else:
            #if the form is not valid 
            return HttpResponse("not valid")
    else:
        form = NameForm()
        return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        p=form.data
        print(p)
        #if the form data is valid it will call auth_enticate function that checks for the authentication
        #  i.e, the user exists or not
        if form.is_valid():

            if auth_enticate(p['your_email'],p['your_password']):
                #if the user exists then it will go to main page 
                # and user name will be shown in place of register and login button
                return render(request,"index.html",{'header_mssg':f"{p['your_name']}"})

            #for invalid credentials it will redirect to main page
            return render(request,"login.html",{"msg":"no user found!","form":form})
        else:
            #bellow code will execute if the form is not valid
            a=form.errors
            print(a)
            login_again="<h3>something is wrong <a href='/check/login'>try again</a></h3>"
            return HttpResponse(login_again)
    else:
        form = NameForm()
        return render(request, 'login.html', {'form': form})
    
#@login_required(login_url="/check/login")
#@permission_required(perm="infun",login_url='check/login')
def infun(request,n):
    print(n,request)
    #this function will execute after clicking "checkin "button

    my_db=get_db()
    my_collection=get_coll_for_user_acc()
    particular_user=my_collection.find_one({"username":n})

    if particular_user==None:
        #n is "NOTDONE" when the user is not logged in still tries to start checkin
        #in that case it will be redirected to login page with a message that the user has to loggedin first
        form=NameForm()
        return render(request,"login.html",{"msg":"FIRST you need to login before that operation","form":form})

    try:
        #if checkin already started user can't checkin again before the previous checkout.
        already_started=particular_user["checkin_time"]
        return HttpResponse(f"you have started your checkin .now you have to <a href='/check/outbus/{n}'>checkout</a> before checking in again")
        
    except Exception as err:
        #when the user is logged in then tries to checkin then checkedin will start perfectly
        checkin= datetime.now()#to get the timedetails of checkin time
        #print(f"checkin time : {checkin}")
        checkin_time=checkin.strftime("%H:%M:%S")
        checkin_month=str(checkin.month)
        checkin_day=str(checkin.day)
        #print(f"checkin time : {checkin_time} checkin month and day : {checkin_month}  {checkin_day} ")
        my_db=get_db()
        my_collection=get_coll_for_user_acc()
        #stores checkin details into the database for future calculation
        my_collection.find_one_and_update(
            {"username":n},
            {"$set":{"checkin_time":{"day":checkin_day,"month":checkin_month,"time":checkin_time}}}
            )
        #after storing it will return to main page
        return render(request,"index.html",{'header_mssg':f"{n}"})

#this function is for "checkout" button
def outfun(request,n):
    #n is "NOTDONE" when the user is not logged in still tries to start checkin
    #in that case it will be redirected to login page with a message that the user has to loggedin first
    my_db=get_db()
    my_collection=get_coll_for_user_acc()
    particular_user=my_collection.find_one({"username":n})

    if particular_user==None:
        form=NameForm
        print("login before")
        return render(request,"login.html",{"msg":"FIRST you need to login before that operation","form":form})
    else:
        #if the user is already logged in and hen tries to checked out then following code will execute
        checkout= datetime.now()#to get the present timing details of checkout
        #print(f"checkout time : {checkout}")
        checkout_time=checkout.strftime("%H:%M:%S")
        checkout_month=checkout.month
        checkout_day=checkout.day
        print(f"checkout time : {checkout_time} checkout month and day : {checkout_month}  {checkout_day} ")

        #checkout function will only work after checkin because a user can only checkout if he/she checkedin before
        #so try exception is being used here.
        #if the user is not checked in before checking out there will be no "checkin_time" entries .
        #so it will generate a key exception
        try:
            particular_user["checkin_time"]
            user_checkin_time=particular_user["checkin_time"]
        except Exception as err:
            #if the exception arise the user will get a httpResponse for checking in before.
            #h/she also can start checkin from the link of the httpresponse(more easy for user)
            #or can goto main page to start checkin if h/she just wants
            return HttpResponse(f"First you have to <a href='/check/inbus/{n}'>checkin<a> before checkout")

        checkin_month=int(user_checkin_time['month'])
        #if the user checked in 2 month ago then checks out now(which is not obvious for ususal case 
        # but somehow h/she forgot to checked out at that time) then the below message will be shown)
        if checkout_month-checkin_month>2:
            return HttpResponse("You have checked in 2 month ago . Give explanation to bus authority with your valid ticket")

        #if the user is loggedin and checked in and then tries to check out between 1 months then this code will going to execute.
        else:
            checkin_day=user_checkin_time["day"]
            checkin_time=user_checkin_time["time"]
            #difference betweeen checkout day and chechin day for calculating bus fair
            diff_day=int(checkout_day)-int(checkin_day)+1
            ch_out_hour,ch_out_min,ch_out_sec=checkout_time.split(":")
            ch_in_hour,ch_in_min,ch_in_sec=checkin_time.split(":")
            #this function will calculate exact time difference (second will not be considered) between checkin and checkout.
            result=subtract(ch_out_hour,ch_out_min,ch_in_hour,ch_in_min,diff_day)
            #price=totalhour*10
            price=result*10
            #store upto 2 decimal values
            price='%.2f' %(price)
            print(price)
            #remove the checkin time details for that user from the database
            my_collection.find_one_and_update({"username":n}, { "$unset": {"checkin_time":1}})
            #return httpResponse for the price 
            #as we didn't integrate the payment method it will redirect to main page after clicking "click here to pay"
            return HttpResponse(f"<p> Your total fair is {price} <br> <a href='/'>click here to pay</a>")
            

def subtract(ch_out_hour,ch_out_min,ch_in_hour,ch_in_min,diff_day):
    #this function will calculate the time difference in hour.
    out_min,out_hour,in_min,in_hour=int(ch_out_min),int(ch_out_hour),int(ch_in_min),int(ch_in_hour)
    if out_min<in_min:
        out_hour-=1
        out_min+=60
    diff_hour=((out_min-in_min)/60)+(out_hour-in_hour)
    return diff_hour*diff_day

