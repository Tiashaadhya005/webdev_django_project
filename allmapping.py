# Route mapping with stoppage 
allroute={
    "route_black":[1,2,3,20,4,5,6,7,8],
    "route_blue":[1,14,15,20,16,17,18,30,19],
    "route_yellow":[1,21,9,22,23,10,24,25,26,27],
    "route_red":[1,9,10,11,12,13],
    "route_green":[1,28,24,25,29,12,30,31]
    }

#mapping of bus with route
bus_with_route={
    "route_black":["bus1", "bus4"],
    "route_blue":["bus2","bus7"],
    "route_yellow":["bus3"],
    "route_red":["bus5","bus6"],
    "route_green":["bus8"]
}

#mapping of busno with no of seat left
bus_with_seat={
    "bus1":{1:5,2:5,3:5,20:5,4:5,5:5,6:5,7:5,8:5},

    "bus2":{1:5,14:5,15:5,20:5,16:5,17:5,18:5,30:5,19:5},

    "bus3":{1:5,21:5,9:5,22:5,23:5,10:5,24:5,25:5,26:5,27:5},

    "bus4":{1:5,2:5,3:5,20:5,4:5,5:5,6:5,7:5,8:5},

    "bus5":{1:5,9:5,10:5,11:5,12:5,13:5},

    "bus6":{1:5,9:5,10:5,11:5,12:5,13:5},

    "bus7":{1:5,14:5,15:5,20:5,16:5,17:5,18:5,30:5,19:5},
    
    "bus8":{1:5,28:5,24:5,25:5,29:5,12:5,30:5,31:5}
}
