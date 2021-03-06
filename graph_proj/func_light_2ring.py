import networkx as nx
import random
import operator
import numpy as np
from ATT.algorithm import surf_tools, tools
import matplotlib.pyplot as plt
from ATT.util import plotfig
from scipy import stats
from ATT.iofunc import iofiles
from os.path import join as pjoin

class light_smallwd(object):
    def __init__(self, nodenum, neighk, p):
        G = nx.watts_strogatz_graph(nodenum, neighk, p)
        self._G = G
        self._nodenum = nodenum
    
    def get_graph(self):
        """
        Get graph
        """
        return self._G

    def pointlight(self, strategy = 'degree'):
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
                green_sdpt = _extract_with_degree(self._G, restpt, option = 'descend')
            elif strategy == 'random':
                green_sdpt = random.choice(list(restpt))
            elif strategy == 'hubvsrandom':
                green_sdpt = _extract_with_degree(self._G, restpt)
            elif strategy == 'hubvsworst':
                green_sdpt = _extract_with_degree(self._G, restpt)
            else:
                raise Exception('Bad parameters')

            green_stablept.add(green_sdpt)
            green_collect.add(green_sdpt)

            # 1 ring neighbor
            green_neigh_1ring = nx.neighbors(self._G, green_sdpt)
            # 2 ring neighbor
            green_neigh_2ring = set()
            for pt in green_neigh_1ring:
                green_neigh_2ring.update(set(nx.neighbors(self._G, pt)))

            green_collect.update(green_neigh_2ring)

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
                blue_sdpt = _extract_with_degree(self._G, restpt, option = 'descend')
            elif strategy == 'random':
                blue_sdpt = random.choice(list(restpt))
            elif strategy == 'hubvsrandom':
                blue_sdpt = random.choice(list(restpt))
            elif strategy == 'hubvsworst':
                blue_sdpt = _extract_with_degree(self._G, restpt, option = 'ascend')
            else:
                raise Exception('Bad parameters')

            blue_collect.add(blue_sdpt)
            blue_stablept.add(blue_sdpt)
            
            # 1 ring neighbour
            blue_neigh_1ring = nx.neighbors(self._G, blue_sdpt)
            # 2 ring neighbour
            blue_neigh_2ring = set()
            for pt in blue_neigh_1ring:
                blue_neigh_2ring.update(set(nx.neighbors(self._G, pt)))          
            blue_collect.update(blue_neigh_2ring)

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

    def seed_degree(self):
        return [G.degree()[i] for i in self.green_stablept], [G.degree()[i] for i in self.blue_stablept]

    def total_seed_degree(self):
        return np.sum(self.seed_degree()[0]), np.sum(self.seed_degree()[1])

    def diff_degree(self):
        return sum(self.seed_degree()[0]) - sum(lscls.seed_degree()[1])

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
    n = 160
    k = 5
    p = 0.9

    j = 1
    while 1:
        iter_time = 500
        print('iteration {}'.format(j))
        j += 1 
        lscls = light_smallwd(n, k, p)
        G = lscls.get_graph()
        diff_hubvsrandom = []
        diff_random = []
        diff_random_degree = []
        lscls.pointlight('hubvsworst')
        diff_hubvsworst = lscls.collect_diff()
        for i in range(iter_time):
            lscls.pointlight('hubvsrandom') 
            diff_hubvsrandom.append(lscls.collect_diff())
            lscls.pointlight('random')
            diff_random.append(lscls.collect_diff())
            diff_random_degree.append(lscls.diff_degree())
        diff_hubvsrandom = np.array(diff_hubvsrandom)
        diff_random = np.array(diff_random)
        p_sig = 1.0*len(diff_hubvsrandom[diff_hubvsrandom>diff_hubvsworst])/len(diff_hubvsrandom)
        if (p_sig<0.01) & (len(diff_hubvsrandom[diff_hubvsrandom<0]) < 0.01*iter_time) & (np.min(diff_hubvsrandom)>-5):
            break      

    G_edges = G.edges()
    G_edges = [list(edge) for edge in G_edges]
    gam_cls = surf_tools.GenAdjacentMatrix()
    adjcent = gam_cls.from_edge(G.edges())

    outparpath = '/home/hellotc/workingdir/outfiles/smallwd_light'
    # Save files
    iocsv_adjcent = iofiles.make_ioinstance(pjoin(outparpath, 'N'+str(n)+'_P'+str(p)+'_K'+str(k)+'_G4_adj.csv'))
    iocsv_edges = iofiles.make_ioinstance(pjoin(outparpath, 'N'+str(n)+'_P'+str(p)+'_K'+str(k)+'_G4_edges.csv'))
    iocsv_adjcent.save(adjcent)
    iocsv_edges.save(np.array(G_edges))
    
    G_degree = np.array(G.degree().values())
    largenode = np.argsort(G_degree)[-6:]
    pos = nx.random_layout(G)
    nx.draw(G, pos, node_color = 'r', with_labels = True)
    plt.show()
    plt.figure()
    nx.draw(G, pos, node_color = 'r', with_labels = True)
    nx.draw_networkx_nodes(G, pos, nodelist = largenode.tolist(), node_color = 'b')
    plt.show()

    plotmat = plotfig.make_figfunction('mat')
    plotmat(adjcent)

    plt.figure()
    plt.hist(G_degree)
    plt.show()

    plotviolin = plotfig.make_figfunction('violin')
    diff_data = np.concatenate((np.expand_dims(diff_hubvsrandom, axis=-1).T, np.expand_dims(diff_random,axis=-1).T))
    plotviolin(diff_data.T, xticklabels = ['StrategyVsRandom', 'Random'])

    plothist = plotfig.make_figfunction('hist')
    plothist(diff_hubvsrandom, [], diff_hubvsworst, p_sig)
    
    plotcorr = plotfig.make_figfunction('corr')
    plotcorr(np.array(diff_random), np.array(diff_random_degree), ['Number of lights', 'Difference of degree'])




 



