import networkx as nx
import random
import operator
import numpy as np

class light_smallwd(object):
    def __init__(self, nodenum, neighk, p):
        G = nx.watts_strogatz_graph(nodenum, neighk, p)
        self._G = G
        self._nodenum = nodenum

    def pointlight(self, strategy = 'degree', option = 'descend'):
        """
        Function for exploring project of light_smallworld
        """
        green_collect = set()
        blue_collect = set()
        green_stablept = set()
        blue_stablept = set()

        allpt = set(range(self._nodenum))
        restpt = allpt.difference(green_collect.union(blue_collect))

        while len(restpt) != 0:
            if strategy == 'degree':
                green_sdpt = _extract_with_degree(self._G, restpt)
            elif strategy == 'random':
                green_sdpt = random.choice(list(restpt))
            else:
                raise Exception('Bad parameters')

            green_stablept.add(green_sdpt)
            green_collect.add(green_sdpt)
            green_neigh = set(nx.neighbors(self._G, green_sdpt))
            green_collect.update(green_neigh)

            inter_collect = green_collect.intersection(blue_collect)
            inter_collect.difference_update(green_stablept.union(blue_stablept))
            blue_collect.difference_update(inter_collect)

            restpt = allpt.difference(green_collect.union(blue_collect))
            if len(restpt) == 0:
                self.green_collect = green_collect
                self.blue_collect = blue_collect
                self.blue_stablept = blue_stablept
                self.green_stablept = green_stablept
                break

            if strategy == 'degree':
                blue_sdpt = _extract_with_degree(self._G, restpt, option = option)
            elif strategy == 'random':
                blue_sdpt = random.choice(list(restpt))
            else:
                raise Exception('Bad parameters')

            blue_collect.add(blue_sdpt)
            blue_stablept.add(blue_sdpt)
            blue_neigh = set(nx.neighbors(self._G, blue_sdpt))
            blue_collect.update(blue_neigh)

            inter_collect = green_collect.intersection(blue_collect)
            inter_collect.difference_update(green_stablept.union(blue_stablept))

            green_collect.difference_update(inter_collect)

            restpt = allpt.difference(green_collect.union(blue_collect))
            
            self.green_collect = green_collect
            self.blue_collect = blue_collect
            self.green_stablept = green_stablept
            self.blue_stablept = blue_stablept

    def collect_diff(self):
        return len(self.green_collect) - len(self.blue_collect)

    def get_seedpt(self):
        return self.green_stablept, self.blue_stablept 

    def get_collect(self):
        return self.green_collect, self.blue_collect

def _extract_with_degree(G, restpt, option = 'descend'):
    """
    """
    if option == 'descend':
        rv = True
    elif option == 'ascend':
        rv = False
    degree_pair = sorted(G.degree().items(), key=operator.itemgetter(1), reverse = rv)
    degree_list = [i[0] for i in degree_pair]
    index_degree_list = [i in list(restpt) for i in degree_list].index(1)
    return degree_list[index_degree_list]

if __name__ == '__main__':
    # This part is to compute difference by strategy to choose seed point with largest degree

    # nodenum = [20, 30, 50, 90, 150, 300]
    # neighk_perct = np.arange(0.1, 1, 0.1)
    # p = 0.2

    # numdif_k = []
    # numdif_n = []
    
    # for node in nodenum:
    #     neighk = [int(i*node) for i in neighk_perct]
    #     for k in neighk:
    #         lscls = light_smallwd(node, k, p)
    #         lscls.pointlight('degree')
    #         numdif_k.append(lscls.collect_diff())
    #     numdif_n.append(numdif_k)
    #     numdif_k = []
    # numdif_n = np.array(numdif_n)
# ---------------------------------------------------------
    # This part is to compute difference in random situation
    # nodenum = 150
    # neighk = 110
    # p = 0.2
    # n_perm = 5000
    # numdif = []

    # lscls = light_smallwd(nodenum, neighk, p)
    # for i in range(n_perm):
    #     lscls.pointlight('random')
    #     numdif.append(lscls.collect_diff())
# ---------------------------------------------------------
    nodenum = 150
    neighk = 10
    p = 0.2
    
    lscls = light_smallwd(nodenum, neighk, p)
    lscls.pointlight('degree', option = 'descend')        
    green_pt, blue_pt = lscls.get_seedpt()
    green_collect, blue_collect = lscls.get_collect()
   

