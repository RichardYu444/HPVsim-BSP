import pandas as pd
import sciris as sc
import numpy as np
import pickle
import hpvsim as hpv
from basePars import base_pars
import networkx as nx
import matplotlib.pyplot as plt
#this funciton takes all the snapshots and returns all the edges ever formed
def get_network(analyzer):
#initialise to store all the edges, it will store a number of pairs (ordered) which are the edges [male id, female id]
    edges = [] #almost certainly not array, as ordering doesnt matter here
    #similarly this is to store all the nodes
    male_arrs = [] 
    female_arrs = []
    for i in range(2): #this 2 is to be changed depending on the number of snapshots, will just hard code this in for now
        people = analyzer.snapshots[i]
        male_arrs.append(people.contacts['m']['m'])
        female_arrs.append(people.contacts['m']['f'])

    #adding an identifier as currently these nodes have overlapping (int) ids
    males = np.concat(male_arrs).astype(str) + "m"
    females = np.concat(female_arrs).astype(str) + "f"
    #networkx takes lists as inputs so:
    edges = list(zip(males, females))
    #getting rid of duplicates
    male_nodes = np.unique(males)
    female_nodes = np.unique(females)
    return (edges, male_nodes, female_nodes)

#we want a snapshot of every year (that we care about)
snap = hpv.snapshot(timepoints=['2000', '2001'])

#run the sim with the snapshots integrated
sim = hpv.Sim(base_pars, analyzers=snap)
sim.run()
# 'a' should have all the snapshots indexed 0 to n for each year
a = sim.get_analyzer()
(edges, nodes) = get_network(a)
print(edges)
print(nodes)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
print(G.edges)
nx.draw(G, with_labels = True, node_size = 1)
plt.show()
## use NetworkX to plot some stuff