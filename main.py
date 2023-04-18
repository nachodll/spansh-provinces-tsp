import os
import math
import googlemaps
from config import MAP_API_KEY
import networkx as nx
import matplotlib.pyplot as plt
import time

TOWN_NAMES_FILE = 'town_names.txt'
TOWN_POSITIONS_FILE = 'town_positions.txt'
TOWN_DIRECTIONS_FILE = 'town_directions.txt'
PROVINCE_NAME = 'Málaga'
EARTH_RADIUS = 6371000

gmaps = googlemaps.Client(key=MAP_API_KEY)

def write_locations_to_file(town_pos):
    print("Writing locations to file...")
    with open(TOWN_POSITIONS_FILE, 'w') as file:
        for (town, (x, y)) in town_pos.items():
            file.write(town + ", " + str(x) + ", " + str(y) + "\n")
    return

def get_locations_from_file():
    print("Getting locations from file...")
    town_pos = {}
    with open(TOWN_POSITIONS_FILE, 'r') as file:
        for line in file:
            (town_name, x, y) = line.split(", ")
            town_pos[town_name] = (float(x), float(y))
    return town_pos

def get_locations_from_api():
    print("Getting locations from API...")
    town_pos = {}
    with open('town_names.txt', 'r') as file:
        for town_name in file:
            town_name_formatted = town_name.rstrip()
            geocode_result = gmaps.geocode(town_name_formatted + ' ' + PROVINCE_NAME)
            location = geocode_result[0]['geometry']['location']
            x = -EARTH_RADIUS * math.cos(location['lat']) * math.cos(location['lng'])
            y = EARTH_RADIUS * math.cos(location['lat']) * math.sin(location['lng'])
            # z coordinate is ignored for simplicity
            town_pos[town_name_formatted] = (x, y)
    return town_pos

def get_locations():
    if os.path.isfile(TOWN_POSITIONS_FILE):
        return get_locations_from_file()
    else:
        town_pos = get_locations_from_api()
        write_locations_to_file(town_pos)
        return town_pos


def write_directions_to_file(town_dir):
    print("Writing directions to file...")
    with open(TOWN_DIRECTIONS_FILE, 'w') as file:
        for ((town1, town2), kms) in town_dir.items():
            file.write(town1 + ", " + town2 + ", " + str(kms) + "\n")

def get_directions_from_file():
    print("Getting directions from file...")
    town_dir = {}
    with open(TOWN_DIRECTIONS_FILE, 'r') as file:
        for line in file:
            (town1, town2, kms) = line.split(", ")
            town_dir[(town1, town2)] = float(kms)
    return town_dir

def get_directions_from_api(town_names):
    print("Getting directions from API...")
    town_dir = {}
    i = 0
    while i < len(town_names):
        time.sleep(0.1) # Wait to avoid query limit
        j = i + 1
        while j < len(town_names):
            direction_result = (gmaps.directions(
                town_names[i] + ' ' + PROVINCE_NAME, 
                town_names[j] + ' ' + PROVINCE_NAME,  
                mode="walking"))
            distance_kms = float(direction_result[0]['legs'][0]['distance']['text'].split(' ')[0])
            town_dir[(town_names[i], town_names[j])] = distance_kms
            j += 1
        print(town_names[i])
        i += 1
    return town_dir

def get_directions(town_names):
    if os.path.isfile(TOWN_DIRECTIONS_FILE):
        return get_directions_from_file()
    else:
        town_dir = get_directions_from_api(town_names)
        write_directions_to_file(town_dir)
        return town_dir
    

def create_graph():
    G = nx.Graph()
    
    # Add nodes
    town_pos = get_locations()
    for (town, (x, y)) in town_pos.items():
        G.add_node(town, pos=(x, y))

    # Add edges
    town_dir = get_directions(list(town_pos.keys()))
    for ((t1, t2), kms) in town_dir.items():
        G.add_edge(t1, t2, weight=kms)

    # Draw nodes
    pos=nx.get_node_attributes(G,'pos')
    nx.draw_networkx_nodes(G, pos, node_size=3)

    # Draw node labels
    node_labels = {k:(v[0], v[1] + 40000) for (k,v) in pos.items()}
    nx.draw_networkx_labels(G, node_labels, font_size=6, font_family="sans-serif")

    # Traveling salesman problem heuristic solution
    tsp = nx.approximation.traveling_salesman_problem
    hamiltonian_path = tsp(G, nodes=G.nodes())
    
    # Draw edges in the cycle
    hamiltonian_edges = []
    for i in range(len(hamiltonian_path)-2):
        hamiltonian_edges.append((hamiltonian_path[i], hamiltonian_path[i+1]))
    nx.draw_networkx_edges(G, pos, edgelist=hamiltonian_edges, width=0.2)

    print(f"Total distance: {round(nx.path_weight(G, hamiltonian_path, weight='weight'),2)} kms")

    # Draw edge labels
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5, font_family="sans-serif")

    plt.axis("off")
    plt.tight_layout()
    plt.show()


create_graph()