import networkx as nx
import random

# Generate small-world network by watts-strogatz method
nodenum = 150
neighk = 10
p = 0.2

G = nx.watts_strogatz_graph(nodenum, neighk, p)

# random seed point
# first start with green point, then blue point
green_collect = set()
blue_collect = set()
stablept = set()

allpt = set(range(nodenum))
restpt = allpt.difference(green_collect.union(blue_collect))

i = 0
while len(restpt)!=0:
    i += 1
    green_sdpt = random.choice(list(restpt))
    stablept.add(green_sdpt)
    green_collect.add(green_sdpt)
    green_neigh = set(nx.neighbors(G, green_sdpt))
    green_collect.update(green_neigh)

    inter_collect = green_collect.intersection(blue_collect)
    inter_collect.difference_update(stablept)
    blue_collect.difference_update(inter_collect)

    restpt = allpt.difference(green_collect.union(blue_collect))
    if len(restpt) == 0:
        break

    blue_sdpt = random.choice(list(restpt))
    blue_collect.add(blue_sdpt)
    stablept.add(blue_sdpt)
    blue_neigh = set(nx.neighbors(G, blue_sdpt))
    blue_collect.update(blue_neigh)

    inter_collect = green_collect.intersection(blue_collect)
    inter_collect.difference_update(stablept)

    green_collect.difference_update(inter_collect)

    restpt = allpt.difference(green_collect.union(blue_collect))




    
   



 
