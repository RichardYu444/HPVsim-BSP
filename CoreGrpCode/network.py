import pandas as pd
import sciris as sc
import numpy as np
import pickle
import hpvsim as hpv
from basePars import base_pars_geno
import networkx as nx
import matplotlib.pyplot as plt
import pathlib
from networkx.algorithms import bipartite


OUTPUT_DIR = r'C:\Users\richa\Documents\HPV sim Project\Code\RandomCode\NetworkCSVs'
seeds = [0]#, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58] #I messed up counting in the original stuff...
years = [
    "2000", #"2001", "2002", "2003", "2004",
    #"2005", #"2006",#
    #"2007", "2008", "2009"
    "2010", #"2011", "2012", "2013", "2014"
    #"2015", #"2016", "2017", "2018", "2019"
    "2020", #"2021", "2022", "2023", "2024"
    "2025", #"2026", "2027", "2028", "2029"
    "2030", #"2031", "2032", "2033", "2034"
    "2035", #"2036", "2037", "2038", "2039",
    "2040"
] #burn in is from 2000 and we target 2040 target

#this funciton takes all the snapshots and returns all the edges ever formed
def get_network(analyzer):
#initialise to store all the edges, it will store a number of pairs (ordered) which are the edges [male id, female id]
    edges = [] #almost certainly not array, as ordering doesnt matter here
    #similarly this is to store all the nodes
    male_arrs = [] 
    female_arrs = []
    for i in range(len(years)): 
        people = analyzer.snapshots[i]
        male_arrs.append(people.contacts['a']['m'])
        female_arrs.append(people.contacts['a']['f'])

    #adding an identifier as currently male and female nodes have overlapping (int) ids
    males = np.concat(male_arrs).astype(str) + "m"
    females = np.concat(female_arrs).astype(str) + "f"
    #networkx takes lists as inputs so:
    edges = list(zip(males, females))
    #getting rid of duplicates
    male_nodes = np.unique(males)
    female_nodes = np.unique(females)
    return (edges, male_nodes, female_nodes)

if __name__ == '__main__':
    outdir = pathlib.Path(OUTPUT_DIR)
    outdir.mkdir(parents=True, exist_ok=True)
    print(f'Outputs will be saved to: {outdir.resolve()}')
    #we want a snapshot of every year (that we care about)
    snap = hpv.snapshot(timepoints= years)
    for seed in seeds:
        base_pars_geno['rand_seed'] = seed
        #run the sim with the snapshots integrated
        sim = hpv.Sim(base_pars_geno, analyzers=snap)
        sim.run()
        # 'a' has all the snapshots indexed 0 to n for each year
        a = sim.get_analyzer()
        (edges, male_nodes, female_nodes) = get_network(a)
        G = nx.Graph()
        G.add_nodes_from(male_nodes, bipartite = 0)
        G.add_nodes_from(female_nodes, bipartite = 1)
        G.add_edges_from(edges)

        #exporting edges etc as a csv for future use
        nodes_df = pd.DataFrame([
            {'node': n, **G.nodes[n], 'seed': seed}
            for n in G.nodes()
        ])
        nodes_df.to_csv(outdir /"all_seeds_graph_nodesTEST.csv", mode = 'a', index= True)    
        edges_df = pd.DataFrame([
            {"source": u, "target": v, **G.edges[u, v], 'seed': seed}
            for u, v in G.edges()
        ])
        edges_df.to_csv(outdir /"all_seeds_graph_edgesTEST.csv", mode = 'a', index= True)
        print(f"seed {seed} is done")
    print('All done!')


#drawing graph with bipartite colour
color = bipartite.color(G)
color_dict = {0:'b',1:'r'}
pos = nx.spring_layout(G, seed=1, k=0.25, iterations=200) 
color_list = [color_dict[i[1]] for i in G.nodes.data('bipartite')]
nx.draw_networkx_nodes(G, pos, node_size=4, node_color = color_list)
nx.draw_networkx_edges(G, pos, width=0.5)
plt.show()


