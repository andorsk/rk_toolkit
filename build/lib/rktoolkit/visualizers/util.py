from .networkx.dendrogram import hierarchy_pos
import math
import numbers
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def draw_graph(G, ax=None, with_labels=True, minsize=100,
                    alpha=300, emult=2, make_axis=False, width=2*math.pi):
    '''Method to draw a general graph of an ontology that is transformed using BaseOntologyTransform.
    Refer to :ref:`HTG transformers<rktoolkit.functions.htg_transformers>` for information on Base Ontology Transform.

    :param G: Transformed Graph to be drawn
    :type G: Graph
    :param ax: Axes to be used for the graph, defaults to None
    :type ax: Axes, optional
    :param with_labels: Parameter to choose if labels need to be shown or not, defaults to True
    :type with_labels: bool, optional
    :param minsize: Minimum size of the graph nodes, defaults to 100
    :type minsize: int, optional
    :param alpha: Alpha index for the graph, defaults to 300
    :type alpha: int, optional
    :param emult: No. of emulations, defaults to 2
    :type emult: int, optional
    :param make_axis: Should axes be made in graph or not, defaults to False
    :type make_axis: bool, optional
    :param width: Horizontal space allocated for this branch - avoids overlap with other branches, defaults to 2*math.pi
    :type width: float, optional
    '''
    if make_axis:
        fig, ax = plt.subplots(figsize=(10,10))

    if ax is None:
        ax = plt.gca()

    #Get the hierachial positions for the graph
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
    '''Method to draw an R-K diagram for a given RK Model.
    Refer to `R-K Model<rktoolkit.models.rkmodel>` for more information. 

    :param rkmodel: R-K model to be drawn a R-K Diagram for.
    :type rkmodel: RKModel
    :param spread: Spread amount for the model, defaults to 1
    :type spread: int, optional
    :param ax: Axes to be used, defaults to None
    :type ax: Axes, optional
    :param with_labels: Parameter to choose if labels need to be shown or not, defaults to True
    :type with_labels: bool, optional
    :param minsize: Minimum size of the nodes, defaults to 100
    :type minsize: int, optional
    :param center_color: Color of the center node, defaults to 'green'
    :type center_color: str, optional
    :param alpha: Alpha index of the graph, defaults to 300
    :type alpha: int, optional
    :param emult: No of emulations, defaults to 2
    :type emult: int, optional
    :param make_axis: Parameter to choose if axes should be made in the model or not, defaults to False
    :type make_axis: bool, optional
    :param width: Horizontal space allocated for this branch - avoids overlap with other branches, defaults to 2*math.pi
    :type width: float, optional
    :param xoff: Offset of X-axis, defaults to 0
    :type xoff: int, optional
    :param yoff: Offset of Y-axis, defaults to 0
    :type yoff: int, optional
    :param color_override: Colors which needs to be overriden, defaults to None
    :type color_override: str, optional
    
    '''
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
