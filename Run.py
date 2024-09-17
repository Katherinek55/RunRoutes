from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
from networkx.algorithms.simple_paths import all_simple_paths
from networkx.exception import NetworkXNoPath
import random
import folium
import warnings

import requests

warnings.filterwarnings("ignore", category=FutureWarning)

# get user input for starting location and desired distance
start = input("Please provide your starting coordinates (latitude, longitude): ")
distance =input("How many miles would you like to go?: ")

# convert disatnce to meters (compatable with open street maps)
distance = float(distance)*1609.34

app = Nominatim(user_agent="tutorial")
location = app.geocode(start)
start_co = (location.latitude, location.longitude)


G = ox.graph_from_point(start_co, distance, network_type= 'walk')

# find a nearby node to start at 
start_node = ox.nearest_nodes(G, start_co[1], start_co[0])

#generates 3 routes and plot on map
def generate_loop_routes(G, start_node, distance, tolerance =0.2):
    routes = []
    nodes = list(G.nodes)
    random.shuffle(nodes)

    #generate map
    start_co = (G.nodes[start_node]['y'], G.nodes[start_node]['x'])
    route_map = folium.Map(location = start_co, zoom_start =14)
    folium.Marker(location= start_co).add_to(route_map)

    for middle_node in nodes:
        if middle_node == start_node:
            continue
        
        try:
            there_length = nx.shortest_path_length(G, start_node, middle_node, weight = 'length')
            back_length = nx.shortest_path_length(G, middle_node, start_node, weight = 'length')
            total = there_length+back_length

            # if the total milage of the route is within the distance * tolerance range, 
            # find a path between the start and middle, then middle to start
            if abs(total - distance) <= distance * tolerance:
                there = nx.shortest_path(G, start_node, middle_node, weight = 'length')
                back = nx.shortest_path(G, middle_node, start_node, weight = 'length')[1:]
                path = there + back

                routes.append((path, total))
                routes_co = [(G.nodes[node]['y'], G.nodes[node]['x'])for node in path]
                folium.PolyLine(routes_co, color ='red', weight = 4, opacity = .8).add_to(route_map)

        except NetworkXNoPath:
            continue

        # stops at 3 routes
        if len(routes) >= 3:
            break

    # prints the length of each route
    for i, route in enumerate(routes, start= 1):
        print(f"length of route {i} = {route[1]/1609.34} miles")
            
    # return 3 routes and map with routes mapped
    return routes, route_map

  

# call method to generate routes and mop
routes_final, route_map = generate_loop_routes(G, start_node, distance)

# saves map as html -- to open map, run open route_maps.html in terminal
route_map.save('route_maps.html')

    








