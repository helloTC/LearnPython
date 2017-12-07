#!/usr/bin/env python
# coding=utf-8

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

node_num = 20
m = 6
# Scale free network, BA
G_scale = nx.barabasi_albert_graph(node_num, m)
G_scale_degree = np.array(G_scale.degree().values())
largenode = np.where(G_scale_degree>0.8*node_num)[0]
pos = nx.random_layout(G_scale)
plt.figure()
nx.draw(G_scale, pos, node_color = 'r')
nx.draw_networkx_nodes(G_scale, pos, nodelist=largenode.tolist(), node_color='b')
plt.show()
plt.figure()
nx.draw(G_scale, pos, node_color = 'r')
plt.show()
plt.figure()
plt.hist(G_scale_degree)
plt.show()
