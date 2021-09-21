from checkinout import views
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import server_error
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import requests
from django.views import View
from django.http import JsonResponse
from .serializers import Serializermodel
from .models import *
from allmapping import *
from svariable import *
from graph_code import *
from forms import *
from unittest.mock import *
from checkinout.views import * 

break_journey_mssg="<h3>There is no direct route . do you want a break jouirney?<a href='/breakjourney'>yes</a></h3>"

def makeBookingForOneRoute(start,end,user_possible_routes,ans_array):
    '''if we have 2 buses for this one particular road then decision should be
     made on the basis of ticket avilability'''

    #route_buses variable will store the bus no for one particular root
    route_buses=bus_with_route[user_possible_routes]
    no_of_buses=len(route_buses)

    #route_direction will store all stoppage serially
    global allroute
    global bus_with_seat
    route_direction=allroute[user_possible_routes]

    reverse_direction_flag=0
    #indexs for starting point and ending point of route_direction array.
    #we need this variable to check if all the stoppage from starting to end have 
    # atleast one empty seat or not
    index1=route_direction.index(start)
    index2=route_direction.index(end)
    if index1>index2:reverse_direction_flag=1

    for num in range(no_of_buses):
        #this variable indicate if break journey needed or not.
        flag_for_break_journey=0 
        
        name_of_the_bus=route_buses[num] 
        busx=bus_with_seat[name_of_the_bus]
        for i in range(index1,index2):
            #we won't include index2 because we don't need to book seat for the stopping location.
            keyy=route_direction[i]
            if busx[keyy]<=0:
                flag_for_break_journey=1
                break
        
        if flag_for_break_journey==0 and reverse_direction_flag==0:
            for i in range(index1,index2):
                keyy=route_direction[i]
                ans_array.append(keyy)
                busx[keyy]-=1
            #have to modify origin dictionary
            return [ans_array,route_buses[num]]
    return None
        
def makebooking(start,end,user_possible_routes):  
    
    localdict={}#a dictionary to store route and pathdifference
    for rou in range(len(user_possible_routes)):
        route_direction=allroute[user_possible_routes[rou]]
        index1=route_direction.index(start)
        index2=route_direction.index(end)
        if index1>index2:continue
        else:
            inddiff=index2-index1
            localdict[user_possible_routes[rou]]=inddiff
    sorted_dict=dict(sorted(localdict.items(), key=lambda item: item[1]))#it will sort the dictionary distance wise
    #print(localdict,sorted_dict)
    for keyy in sorted_dict.keys():
        #we will check for the every buses of this route
        ans_array=makeBookingForOneRoute(start,end,keyy,[])
        if ans_array!=None:
            return ans_array
    return None

#this function is for direct routed user
def choice_of_user(serialized_data):

    StartingLocation=int(serialized_data.data['StartingLocation'])
    EndLocation=int(serialized_data.data['EndLocation'])


    #array for storing all direct routes that include both startpoint and endpoint
    user_possible_routes=[]

    #if start and end location is at same route and store that routre inside user_possible_routes
    for keyy in allroute.keys():
        if StartingLocation in allroute[keyy] and EndLocation in allroute[keyy]:
            user_possible_routes.append(keyy)
    total_no_of_possible_routes=len(user_possible_routes)
    #print(total_no_of_possible_routes,user_possible_routes)

    #if there is no route that has both start and end location then this if condition will be follwed and the user will get a option for break jouirney
    if (total_no_of_possible_routes==0):
        result=False

    #if there is only one route that has both start and end location then this if condition will be follwed
    elif(total_no_of_possible_routes==1):
        ans_array=makeBookingForOneRoute(StartingLocation,EndLocation,user_possible_routes[0],[])
        result=True
        #user_allotted_route=user_possible_routes[0]


    #if there is more than one route that has both start and end location then this else condition will be follwed
    else:
        ans_array=makebooking(StartingLocation,EndLocation,user_possible_routes)
        if ans_array!=None:
            #user_allotted_route=result_1
            result=True
        else:result=False

    if result==True:return ans_array
    if result==False:return None



def index(request):
    return render(request,'index.html')

def mocked_inbus():
    return "checkin_time"


#@patch('checkinout.views.infun', side_effect=mocked_inbus) 
##bookseat() got multiple values for argument 'username'
#@rest_framework.decorators.api_view["GET","POST"]
class Bookseat(View):
    def post(request,username):
        print("request",request,"username:",username)
        sl=request.POST.get("StartingLocation","")
        serializer_data=Serializermodel(data=request.data)
        if serializer_data.is_valid():
            res=choice_of_user(serializer_data)
            pp={'StartingLocation':request.data['StartingLocation'],'EndLocation':request.data['EndLocation']}
            if res!=None:
                #print("che: ",Serializer.validated_data)
                Serializermodel.create(self=Serializermodel,validated_data=pp)
                #content = JSONRenderer().render(serializer_data.data)
                station_name=get_keys_from_value(res[0])
                route=get_route(res[1])
                #doubt for mock_function
                #response_for_checkin = requests.get(f'http://127.0.0.1:8000/check/inbus/{username}').checkin_time
                #print("checkinresponse:",response_for_checkin)
                json_response={
                    "status":status.HTTP_202_ACCEPTED,
                    "data":{
                        "User":username,
                        "route":route,
                        "starting_station":serializer_data.data['StartingLocation'],
                        "ending_station":serializer_data.data['EndLocation'],
                        "path":station_name,
                        "bus":res[1],
                        #"fair":"",
                        #"check-in":response_for_checkin,
                    },
                    "message":"your ticket has been booked",
                }
                return JsonResponse(json_response,safe=False)#json_dumps_params={"StartingLocation":res})#json_dumps_params={"your journey stoppage":res})
                return HttpResponse(f"Successfully booked seat in {res}")
            else:
                StartingLocation=int(serializer_data.data['StartingLocation'])
                EndLocation=int(serializer_data.data['EndLocation'])
                return HttpResponse(f"<h3>There is no direct route . do you want a break jouirney?<a href='/breakjourney/{username}/{StartingLocation}-{EndLocation}'>yes</a></h3>")
        return Response(serializer_data.errors)
    def get(self,request,username):
        print("chex",username)
        if(username=="NOTDONE"):
            form=NameForm()
            return render(request,"login.html",{"msg":"FIRST you need to login before that operation","form":form})
        return render(request,'bookticket.html',{"header":username})



def graphjourney(request,username,stations):
    station1,station2=stations.split("-")
    pp={'StartingLocation':station1,'EndLocation':station2}
    station1,station2=int(station1),int(station2)
    g=Graph()
    allpath=g.findpaths(station1,station2,[])
    allpath.sort(key=len)
    if allpath==None:
        start_station=get_keys_from_value(station1)[0]
        stop_station=get_keys_from_value(station2)[0]
        json_response={
            "message":"No ticket avilable for your journey",
        }
        return JsonResponse(json_response,safe=False)
    else:
        no_ticket_flag=0
        stop_int_val=[]
        for i in range(len(allpath)):
            individual_path=allpath[i]
            possible=[]
            for key_1 in allroute.keys():
                if individual_path[0]in allroute[key_1] and individual_path[1] in allroute[key_1]:
                    if allroute[key_1].index(individual_path[0])<allroute[key_1].index(individual_path[1]):
                        possible.append(key_1)
            #busx[keyy]-=1
            for kk in possible:
                no_ticket_flag=0
                ans=makeBookingForOneRoute(individual_path[0],individual_path[1], kk,[])
                if ans==False:
                    no_ticket_flag=1
                    continue
                else:
                    for jj in range(2,len(individual_path)):
                        if individual_path[jj] in allroute[kk]: #that means in same path
                            #print(individual_path[jj-1],individual_path[jj],kk)
                            ans_2=makeBookingForOneRoute(individual_path[jj-1],individual_path[jj],kk,[])
                            if ans_2==None:
                                no_ticket_flag=1
                                break
                            stop_int_val.append(ans_2[0][0])
                        else: #means a junction 
                            for key_2 in allroute.keys():
                                if individual_path[jj-1]in allroute[key_2] and individual_path[jj] in allroute[key_2]:
                                    #print(individual_path[jj-1],individual_path[jj],key_2)
                                    ans_2=makeBookingForOneRoute(individual_path[jj-1],individual_path[jj],key_2,[])
                                    if ans_2==None:
                                        no_ticket_flag=1
                                        break
                                    stop_int_val.append(ans_2[0][0])
                                    kk=key_2
                            if no_ticket_flag==1:break
                if no_ticket_flag==0:break
            if no_ticket_flag==0:break

        start_station=get_keys_from_value_for_one(station1)
        stop_station=get_keys_from_value_for_one(station2)   
        if no_ticket_flag==1:
            json_response={
                "message":"No ticket avilable for your journey",
            }
            return JsonResponse(json_response,safe=False)
        else:
            Serializermodel.create(self=Serializermodel,validated_data=pp)
            #station_name=get_keys_from_value(ans_2[0])
            stop_int_val.insert(0,station1)
            stop_int_val.append(station2)
            station_name=get_keys_from_value(stop_int_val)
            print(stop_int_val,station_name)
            json_response={
                "status":status.HTTP_202_ACCEPTED,
                "data":{
                    "User":username,
                    "starting_station":start_station,
                    "ending_station":stop_station,
                    "path":station_name,
                    #"fair":"",
                    #"check-in":response_for_checkin,
                },
                "message":"your ticket has been booked",
            }
            return JsonResponse(json_response,safe=False)
        #return HttpResponse("Your ticket has been booked.")

def get_keys_from_value(val):
    ans_array=[]
    for i in val:
        for k, v in stoppagename.items():
            if v == int(i):
                ans_array.append(k)
    return ans_array

def get_route(val):
    for k, v in bus_with_route.items():
        for i in v:
            if i==val:
                return k

def get_keys_from_value_for_one(val):
    for k, v in stoppagename.items():
        if v == val:
            return k


