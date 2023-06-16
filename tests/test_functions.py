import copy

import cript
import pydot
import pytest

import cript_graph


@pytest.fixture(scope="session")
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """
    with cript.API(host=None, token=None) as api:
        yield api


@pytest.fixture(scope="function")
def example_cript_graph(cript_api):
    my_experiment = cript.Experiment(name="my experiment name")
    my_collection = cript.Collection(name="my collection name", experiment=[my_experiment])
    my_project = cript.Project(name="my Project name", collection=[my_collection])
    identifiers = [{"bigsmiles": "123456"}]
    my_material = cript.Material(name="my material", identifiers=identifiers)
    my_project.material += [my_material]

    my_computation = cript.Computation(name="my computation name", type="analysis")

    property = cript.Property("modulus_shear", "value", 5.0, "GPa", computation=[my_computation])
    my_material.property += [property]

    computation2 = copy.deepcopy(my_computation)
    computation2.name = "computation 2, new"
    property2 = cript.Property("modulus_loss", "value", 5.0, "GPa", computation=[computation2])
    my_material.property += [property2]

    cript.add_orphaned_nodes_to_project(my_project, my_experiment)
    my_project.validate()
    return my_project


@pytest.fixture(scope="function")
def networkx_graph(example_cript_graph):
    graph = cript_graph.get_networkx_graph(example_cript_graph)
    return graph


def test_networkx_graph(networkx_graph):
    graph = networkx_graph
    assert len(graph.nodes) == 8
    assert len(graph.edges) == 9


def test_dot_graph(networkx_graph):
    graph = networkx_graph
    dot_string = cript_graph.get_dot_graph(graph)
    assert isinstance(dot_string, str)
    assert len(dot_string) == 1866
    pydot_graph = pydot.graph_from_dot_data(dot_string)
    assert pydot_graph
