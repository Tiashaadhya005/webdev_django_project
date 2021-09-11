from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import server_error
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Serializermodel
from .models import Bus_booking
from allmapping import *
from svariable import *
from graph_code import *
  

break_journey_mssg="<h3>There is no direct route . do you want a break jouirney?<a href='/breakjourney'>yes</a></h3>"

def makeBookingForOneRoute(start,end,user_possible_routes):
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
        for i in range(index1,index2): #we won't include index2 because we don't need to book seat for the stopping location.
            keyy=route_direction[i]
            if busx[keyy]<=0:
                flag_for_break_journey=1
                break
        
        if flag_for_break_journey==0 and reverse_direction_flag==0:
            for i in range(index1,index2):
                keyy=route_direction[i]
                busx[keyy]-=1
            #have to modify origin dictionary
            return True
    return False
        
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
        if makeBookingForOneRoute(start,end,keyy)==True:
            return keyy
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
        result=makeBookingForOneRoute(StartingLocation,EndLocation,user_possible_routes[0])
        user_allotted_route=user_possible_routes[0]


    #if there is more than one route that has both start and end location then this else condition will be follwed
    else:
        result_1=makebooking(StartingLocation,EndLocation,user_possible_routes)
        if result_1!=None:
            user_allotted_route=result_1
            result=True
        else:result=False

    if result==True:return user_allotted_route
    if result==False:return None



def index(request):
    return render(request,'index.html')



@api_view(['GET','POST'])
def bookseat(request):
    if request.method=='POST':
        serializer_data=Serializermodel(data=request.data)
        if serializer_data.is_valid():
            res=choice_of_user(serializer_data)
            if res!=None:
                # print(Serializer.validated_data)
                #Serializermodel.create(Serializermodel,validated_data=serializer_data)
                return HttpResponse(f"Successfully booked seat in {res}")
                return Response({'msg':"Ticket booked"})
            else:return HttpResponse(break_journey_mssg)
        return Response(serializer_data.errors)
    else:
        return render(request,'bookticket.html')


@api_view(['GET','POST'])
def graphjourney(request):
    if request.method=='POST':
        serialized_data=Serializermodel(data=request.data)
        if serialized_data.is_valid():
            StartingLocation=int(serialized_data.data['StartingLocation'])
            EndLocation=int(serialized_data.data['EndLocation'])
            #print(StartingLocation,EndLocation)

            g=Graph()
            #return HttpResponse("ok")
            allpath=g.findpaths(StartingLocation,EndLocation,[])
            allpath.sort(key=len)
            #print(allpath)
            if allpath==None:return HttpResponse("No path avilable")
            else:
                no_ticket_flag=0
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
                        ans=makeBookingForOneRoute(individual_path[0],individual_path[1], kk)
                        if ans==False:
                            no_ticket_flag=1
                            continue
                        else:
                            for jj in range(2,len(individual_path)):
                                if individual_path[jj] in allroute[kk]: #that means in same path
                                    #print(individual_path[jj-1],individual_path[jj],kk)
                                    ans_2=makeBookingForOneRoute(individual_path[jj-1],individual_path[jj],kk)
                                    if ans_2==False:
                                        no_ticket_flag=1
                                        break
                                else: #means a junction 
                                    for key_2 in allroute.keys():
                                        if individual_path[jj-1]in allroute[key_2] and individual_path[jj] in allroute[key_2]:
                                            #print(individual_path[jj-1],individual_path[jj],key_2)
                                            ans_2=makeBookingForOneRoute(individual_path[jj-1],individual_path[jj],key_2)
                                            if ans_2==False:
                                                no_ticket_flag=1
                                                break
                                            kk=key_2
                                        if no_ticket_flag==1:break
                                if no_ticket_flag==1:break
                        if no_ticket_flag==1:continue
                        if no_ticket_flag==0:break
                    if no_ticket_flag==0:break
                if no_ticket_flag==1:
                    return HttpResponse("No ticket avilable for your journey")
                else:
                    return HttpResponse("Your ticket has been booked.")


        else:return HttpResponse("not valid")
    else:
        return render(request,'breakjourneyform.html')



