import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import random

# Reproducible
seed = 7
random.seed(seed)
np.random.seed(seed)

# ---- Specs ----
N = 500
core_frac = 0.60
n_core = int(N * core_frac)          # 300
n_clusters = 10

n_blue = N // 2  # 250
n_red  = N - n_blue

blue_nodes = [f"B{i}" for i in range(n_blue)]
red_nodes  = [f"R{i}" for i in range(n_red)]

# Core = 150 blue + 150 red
core_blue = blue_nodes[:n_core//2]
core_red  = red_nodes[:n_core//2]

# Peripheral = remaining 100 blue + 100 red -> 10 clusters of 10+10
periph_blue = blue_nodes[n_core//2:]
periph_red  = red_nodes[n_core//2:]
random.shuffle(periph_blue)
random.shuffle(periph_red)

clusters = []
for ci in range(n_clusters):
    cb = periph_blue[ci*10:(ci+1)*10]
    cr = periph_red[ci*10:(ci+1)*10]
    clusters.append((cb, cr))

# ---- Build bipartite graph ----
G = nx.Graph()

for n in core_blue:
    G.add_node(n, bipartite=0)
for n in core_red:
    G.add_node(n, bipartite=1)

for ci, (cb, cr) in enumerate(clusters):
    for n in cb:
        G.add_node(n, bipartite=0, cluster=ci)
    for n in cr:
        G.add_node(n, bipartite=1, cluster=ci)

# Core edges: each core-blue node ~6 links into core-red
for b in core_blue:
    for r in random.sample(core_red, k=6):
        G.add_edge(b, r)

# Intra-cluster edges: each cluster-blue node links to ~3 cluster-red nodes
for ci, (cb, cr) in enumerate(clusters):
    for b in cb:
        for r in random.sample(cr, k=3):
            G.add_edge(b, r)

# Cluster-to-core bridges: few links
for ci, (cb, cr) in enumerate(clusters):
    for _ in range(2):
        G.add_edge(random.choice(cb), random.choice(core_red))
    for _ in range(2):
        G.add_edge(random.choice(cr), random.choice(core_blue))

# Very sparse inter-cluster edges
for _ in range(2):
    i, j = random.sample(range(n_clusters), 2)
    G.add_edge(random.choice(clusters[i][0]), random.choice(clusters[j][1]))

# ---- Structured layout ----
pos = {}
Gc = G.subgraph(core_blue + core_red)
core_pos = nx.spring_layout(Gc, seed=seed, k=0.35, iterations=120)
for n, p in core_pos.items():
    pos[n] = np.array(p) * 0.8

ring_R = 3.6
for ci, (cb, cr) in enumerate(clusters):
    H = G.subgraph(cb + cr)
    local_pos = nx.spring_layout(H, seed=seed+ci, k=0.8, iterations=80)

    pts = np.array(list(local_pos.values()))
    pts = pts - pts.mean(axis=0)
    scale = np.max(np.linalg.norm(pts, axis=1)) if len(pts) else 1.0
    pts = pts / (scale if scale > 0 else 1.0) * 0.55

    angle = 2*np.pi*ci/n_clusters
    center = np.array([ring_R*np.cos(angle), ring_R*np.sin(angle)])
    for node, p in zip(local_pos.keys(), pts):
        pos[node] = center + p

# ---- Draw: make edges MORE prominent ----
blues = [n for n, d in G.nodes(data=True) if d["bipartite"] == 0]
reds  = [n for n, d in G.nodes(data=True) if d["bipartite"] == 1]

fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")

# Increased alpha + slightly thicker edges
nx.draw_networkx_edges(G, pos, ax=ax, width=0.6, alpha=0.5, edge_color="black")
nx.draw_networkx_nodes(G, pos, nodelist=blues, ax=ax, node_color="tab:blue", node_size=7, linewidths=0)
nx.draw_networkx_nodes(G, pos, nodelist=reds,  ax=ax, node_color="tab:red",  node_size=7, linewidths=0)

ax.set_axis_off()
ax.set_title("Core + clusters", fontsize=14)

plt.tight_layout()
plt.show()