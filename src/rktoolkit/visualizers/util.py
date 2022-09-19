from .networkx.dendrogram import hierarchy_pos
import math
import numbers
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def draw_graph(G, ax=None, with_labels=True, minsize=100,
                    alpha=300, emult=2, make_axis=False, width=2*math.pi):

    if make_axis:
        fig, ax = plt.subplots(figsize=(10,10))

    if ax is None:
        ax = plt.gca()

    pos = hierarchy_pos(G, 'root', width = width, xcenter=0)
    pos = {u:(r*math.cos(theta),r*math.sin(theta)) for u, (theta, r) in pos.items()}
    colors = [ n[1].get('color', 'black') for n in list(G.nodes.items())]

    sizes = []
    for n in list(G.nodes.items()):
        v = n[1].get("value", 1)
        if not isinstance(v, numbers.Number):
            v = 1
        v+=1
        sizes.append(v)

    sizes = np.array(sizes)
    sizes = sizes ** 5 #np.exp(sizes)
    sizes = (sizes - sizes.min()) / (sizes.max()-sizes.min())
    sizes *= alpha
    sizes += minsize
    sizes = np.where(np.isnan(sizes), minsize, sizes)
    nx.draw(G, pos=pos, with_labels=with_labels,
            font_size=10, node_size=sizes, ax=ax, node_color = colors, edgecolors = 'black')
    nx.draw_networkx_nodes(G, pos=pos, nodelist = ['root'],
                           node_color = 'green', ax=ax, node_size = sizes.max()*emult)

# TODO refactoring: should look like this:
# draw_graph <= draws a general graph
# draw_graph_with_structure <= draws a graph with
# draw_rk_diagram <= draws an rk model. minimal redudant code.
# there was an initial optiization that happened in the
# visualizers module, but that probably needs to be re-evaluated
# and merged with some of the work here.
def draw_rk_diagram(rkmodel, spread=1, ax=None, with_labels=True, minsize=100, center_color='green',
                    alpha=300, emult=2, make_axis=False, width=2*math.pi, xoff=0, yoff=0, color_override=None):
    if make_axis:
        fig, ax = plt.subplots(figsize=(10,10))

    if ax is None:
        ax = plt.gca()

    # indexing
    nodes = list(rkmodel.G.nodes)
    g = rkmodel.get()
    node_subset = list(g.nodes)
    selected_indexes = [nodes.index(n) for n in node_subset]

    # positioning
    structural_pos = hierarchy_pos(rkmodel.G, 'root', width = width, xcenter=0)
    structural_pos = {u:(r*math.cos(theta)*spread,r*math.sin(theta)*spread) for u, (theta, r) in structural_pos.items()}

    # color
    structural_colors = [ rkmodel.G.nodes[n].get('color','black') for n in nodes]
    filtered_colors = [structural_colors[i] for i in selected_indexes]
    if color_override is not None:
        if isinstance(color_override, str):
            filtered_colors = [color_override] * len(filtered_colors)

    # filter node to only ones that show after getting the rkm
    filtered_pos = {k: structural_pos[k] for k in node_subset}

    # update
    for k,v in filtered_pos.items():
        filtered_pos[k] = [v[0]+xoff, v[1]+yoff]

    def _get_sizes(subset, defaultN=1, minsize=1):
        # convert all nodes into numeric values
        sizes = []
        for n in node_subset:
            v = rkmodel.G.nodes[n].get("value", 1)
            if not isinstance(v, numbers.Number):
                v = defaultN
            v+=minsize
            sizes.append(v)
        return sizes

    def _resize(sizes):
        sizes = np.array(sizes)
        sizes = sizes ** 5 #np.exp(sizes)
        sizes = (sizes - sizes.min()) / (sizes.max()-sizes.min())
        sizes *= alpha
        sizes += minsize
        sizes = np.where(np.isnan(sizes), minsize, sizes)
        return sizes

    sizes = _get_sizes(node_subset)
    sizes = _resize(sizes)

    nx.draw(g, pos=filtered_pos, with_labels=with_labels,
            font_size=10, node_size=sizes, ax=ax, node_color = filtered_colors, edgecolors = 'black')

    nx.draw_networkx_nodes(g, pos=filtered_pos, nodelist = ['root'],
                           node_color = center_color, ax=ax, node_size = sizes.max()*emult)
