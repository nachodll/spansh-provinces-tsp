# spanish-provinces-tsp

Find the fastest (heuristic) cycle to visit all towns in a certain sapanish province. 
1. It uses ***town_names.txt*** as input with the names of all towns in the province.
    - **preprocessing_script.py** is used to format the data in case names are separated by commas or whitespaces.
2. It uses **networkx** to model a graph with all the towns, their respective position and the distance between all of them.
    - Each town is a node (with a position).
    - Each edge weight is distance in kms (complete graph is assumed).
3. **Googlemaps Geocoding API** is used to get the geographical coordinates of each town (longitude and latitude), which is later translated to cartesian coordinates (x,y) in order to draw the graph as a map.
    - ***town_positions.txt*** is used as cache to avoid unnecessary api calls.
4. **Googlemaps Directions API** is used to get the walking distance between each pair of towns. Each distance in kms is each edge weight.
    - ***town_directions.txt*** is used as cache to avoid unnecessary api calls.
5. **nx.approximation.traveling_salesman_problem** is used to find the fastest cycle heuristicly.
6. The nodes and edges in the cycle are drawn using **matplotlib.pyplot**.



### Limitations
- Assumes walking
- Requires previous knowledge (list of towns)
- Googlemaps directions api limit make it slow (better with cache)
- Assuming a complete graph makes it complexity O(n*(n-1)/2).
