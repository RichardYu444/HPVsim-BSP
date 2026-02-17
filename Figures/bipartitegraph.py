import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

B = nx.Graph()

#set up two sets of bipartite networks
A_nodes = [f"A{i}" for i in range(4)]
B_nodes = [f"B{i}" for i in range(6)]

B.add_nodes_from(A_nodes, bipartite = 0)
B.add_nodes_from(B_nodes, bipartite = 1)

edges = [
    ("A0","B0"), ("A0","B1"), ("A0","B3"),
    ("A1","B1"), ("A1","B2"),
    ("A2","B2"), ("A2","B4"),
    ("A3","B0"), ("A3","B4"), ("A3","B5"),
]

B.add_edges_from(edges)

colour_map = []
for n in B.nodes():
    if B.nodes[n].get("bipartite") == 0:
        colour_map.append("tab:purple")
    elif B.nodes[n].get("bipartite") == 1:
        colour_map.append("tab:orange")
    else:
        print("error: bipartite code not found")

nx.draw(B, with_labels = True,
        node_color = colour_map,
        node_size = 1000,
        font_weight='bold'
        )

plt.title("Random Layout Bipartite Graph")
plt.show()

pos = {}
for i, n in enumerate(A_nodes):
    pos[n] = (1, i)

for i, n in enumerate(B_nodes):
    pos[n] = (1.1, i)

nx.draw(B, with_labels = True,
        node_color = colour_map,
        pos = pos,
        node_size = 5000,
        font_weight='bold'
        )
plt.title("Sorted Layout Bipartite Graph")
plt.figure(figsize=(3, 6))
plt.show()