import networkx as nx
import random

class light_smallwd(object):
    def __init__(self, nodenum, neighk, p):
        G = nx.watts_strogatz_graph(nodenum, neighk, p)
        self._G = G

    def pointlight(self):
        """
        Function for exploring project of light_smallworld
        """

        green_collect = set()
        blue_collect = set()
        stablept = set()

        allpt = set(range(nodenum))
        restpt = allpt.difference(green_collect.union(blue_collect))

        while len(restpt) != 0:
            green_sdpt = random.choice(list(restpt))
            stablept.add(green_sdpt)
            green_collect.add(green_sdpt)
            green_neigh = set(nx.neighbors(self._G, green_sdpt))
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
            blue_neigh = set(nx.neighbors(self._G, blue_sdpt))
            blue_collect.update(blue_neigh)

            inter_collect = green_collect.intersection(blue_collect)
            inter_collect.difference_update(stablept)

            green_collect.difference_update(inter_collect)

            restpt = allpt.difference(green_collect.union(blue_collect))
            
            self.green_collect = green_collect
            self.blue_collect = blue_collect
            self.stablept = stablept

    def collect_diff(self):
        return len(self.green_collect) - len(self.blue_collect)

if __name__ == '__main__':
    nodenum = 150
    neighk = 10
    p = 0.2

    lscls = light_smallwd(nodenum, neighk, p)
    lscls.pointlight()
    numdif = lscls.collect_diff()
        



