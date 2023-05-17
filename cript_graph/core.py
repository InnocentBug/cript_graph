import networkx as nx


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
    pass


def get_dot_graph(graph, include_in_label=["node", "name", "key"]):
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
    pass
