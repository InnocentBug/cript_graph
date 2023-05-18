# CRIPT Graph operation Plugin for the Python SDK

This is a plugin designed to operate in tandem with the Python SDK of the CRIPT project.
The Python SDK can be found here: https://github.com/C-Accel-CRIPT/Python-SDK
And more information about the CRIPT project in general can be found here: https://criptapp.org/
And the corresponding scientific publication: [Walsh, D. J., Zou, W., Schneider, L., Mello, R., Deagen, M. E., Mysona, J., ... & Olsen, B. D. (2023). Community Resource for Innovation in Polymer Technology (CRIPT): A Scalable Polymer Material Data Structure.] (https://pubs.acs.org/doi/full/10.1021/acscentsci.3c00011)

This plugin a number of helper functions, that can make dealing with the data graphs of CRIPT significantly easier.

## NetworkX graphs

[NetworkX](https://networkx.org/) is a popular python package for dealing with graphs.
This plugin offers a conversion function, that converts a CRIPT SDK data graph into a networkx graph.

```python
import cript
import cript_graph

with cript.API(None, None) as api:
   # CRIPT SDK code to build (or download) the data graph
   project = cript.Project(...)
   # ...
   networkx_graph = cript_graph.get_networkx_graph(project)
   # Networkx graph operations
   print(netowrkx_graph.nodes)
   print(netowrkx_graph.edges)
```

See documentation of `get_networkx_graph` for details about the resulting graph.

## Graphiz Dot vizualization

Vizualizing the entire data graph of CRIPT can be challenging.
The website front-end offers an amazing graph view, but sometimes more details are required.
For example for debugging.

In this situation, it can be helpful to use this provide tool to generate a visual representation of the data graph.
For this we identify the [Graphviz](https://graphviz.org/) dot tool as helpful.

```python
import cript
import cript_graph

with cript.API(None, None) as api:
   # CRIPT SDK code to build (or download) the data graph
   project = cript.Project(...)
   # ...
   # Create intermediate networkx graph
   networkx_graph = cript_graph.get_networkx_graph(project)
   # Generate the graph representation in the dot language
   dot_string = cript_graph.get_dot_graph(graph)
```

This [dot language](https://graphviz.org/doc/info/lang.html) string can either be written to disk

```python
with open("graph.dot", "w") file_handle:
   file_hanle.write(dot_string)
```

And then converted into an SVG graph on the command line

```bash
dot -Tsvg graph.dot > graph.svg
```

Or [pydot](https://github.com/pydot/pydot) can be used to handle the generation of the vizualization from inside python.

```python
import pydo
pydot_graph = pydot.graph_from_dot_data(dot_string)
pydot_graph.write_svg("graph.svg")
```

A resulting graph might look like:

![Example Graph of CRIPT vizualized via Graphviz dot](./assests/graph.svg)
<img src="./assests/graph.svg">
