from math import sqrt

import cript
import networkx as nx


def _determine_darkness_from_hex(color):
    """
    Determine the darkness of a color from its hex string.

    Arguments:
    ----------
    color: str
       7 character string with prefix `#` followed by RGB hex code.

    Returns: bool
       if the darkness is below half
    """
    # If hex --> Convert it to RGB: http://gist.github.com/983661
    assert color[0] == "#"
    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    # HSP (Highly Sensitive Poo) equation from http://alienryderflex.com/hsp.html
    hsp = sqrt(0.299 * red**2 + 0.587 * green**2 + 0.114 * blue**2)
    return hsp < 127.5


CRIPT_colors = {
    "Group": "#775A55",
    "User": "#BFB2AB",
    "Project": "#20262C",
    "Collection": "#576575",
    "Experiment": "#ADAFBD",
    "Inventory": "#E5E6EB",
    "Material": "#275497",
    "Process": "#951919",
    "Data": "#2D9742",
    "Computation": "#FFCC00",
    "ComputationProcess": "#593196",
    "Reference": "#FFFFFF",
    "Software": "#FFFFFF",
}


def get_networkx_graph(root_node) -> nx.DiGraph:
    """
    This function converts a cript node graph into a networkx DiGraph.
    After this conversion, the networkx graph can be used for graph operations like, search and traversal.
    The resulting graph structure is static and doesn't evolve even as the underlying cript graph might be changed by the user.
    Objects are referenced as shallow copy, so simple changes that do not change the graph connectivity are dynamic.

    Arguments:
    ----------
    root_node: cript.BaseNode
         Root node of the graph that needs to be converted.
         Any child of the root node and their children are included in the graph and directionally connected.

    Retruns: networkx.DiGraph
         The nodes are the actual python objects and no further node attributes are available.
         Edges carry an `attribute` that labels the attribute of the parent node which connects them.
    """

    def add_node(G, node):
        """
        Helper function, that adds a node and all its edges to graph.
        Calls itself recursively on all BaseNodes.
        """
        if node in G.nodes:
            return G
        G.add_node(node)
        for field in node._json_attrs.__dataclass_fields__:
            attr_list = getattr(node._json_attrs, field)
            if not isinstance(attr_list, list):
                attr_list = [attr_list]
            for attr in attr_list:
                if isinstance(attr, cript.nodes.core.BaseNode):
                    G = add_node(G, attr)
                    G.add_edge(node, attr, attribute=field)
        return G

    G = nx.DiGraph()
    add_node(G, root_node)
    return G


def get_dot_graph(graph, include_in_label=["node_type", "name", "key"]):
    """
    Converts a networkx representation (see `get_networkx_graph`) of a CRIPT data graph
    into a description of the Graphiz Dot language (https://www.graphviz.org/doc/info/lang.html).
    This can subsequently vizualized via the graphiz `dot` or related tools.

    The aim of this vizualization is to check graphs for correctness and intent.
    The CRIPT front end website produces better, more navigatable graphs.

    Arguments:
    ----------
    graph: networkx.DiGraph
        Graph build from `get_networkx_graph` of a CRIPT Python SDK generated data graph.
    include_in_label: List[str]
        List of string attributes that are to be included into the labels of nodes.
        This allows flexibility to identify nodes in the vizualization of the final graph.

    Returns: str
    --------
    String in the dot language that can be used to invoke the graph vizualization via graphiz tools.
    """
    dot_str = "strict digraph { \n"
    for node in graph.nodes:
        label = ""
        for name in include_in_label:
            try:
                label += f"{getattr(node, name)} "
            except AttributeError:
                pass
            extra_attr = ""
        if node.node_type in CRIPT_colors:
            color = CRIPT_colors[node.node_type]
            extra_attr = f'style=filled, fillcolor="{color}", '
            if _determine_darkness_from_hex(color):
                extra_attr += "fontcolor=white,"

        dot_str += f'"{node.uid}" [{extra_attr} label="{label}"];\n'

    for edge in graph.edges():
        edge_data = graph.get_edge_data(*edge)
        dot_str += f"\"{edge[0].uid}\" -> \"{edge[1].uid}\" [label={edge_data['attribute']}];\n"
    dot_str += "}\n"
    return dot_str
