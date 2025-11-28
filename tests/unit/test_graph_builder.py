import pytest
from os_explorer.graph.builder import GraphBuilder
from os_explorer.graph.model import Node

def test_add_node():
    gb = GraphBuilder("p1", "proj1")
    node = Node(id="s1", type="server", name="s1", label="s1")
    gb.add_node(node)
    assert "s1" in gb.graph.nodes
    assert gb.graph.nodes["s1"].type == "server"

def test_add_edge():
    gb = GraphBuilder("p1", "proj1")
    gb.add_edge("s1", "v1", "attached")
    assert len(gb.graph.edges) == 1
    assert gb.graph.edges[0].from_node == "s1"
    assert gb.graph.edges[0].to_node == "v1"
    assert gb.graph.edges[0].type == "attached"

def test_link_server_volumes():
    gb = GraphBuilder("p1", "proj1")
    server_id = "s1"
    volumes = [
        {"id": "v1", "attachments": [{"server_id": "s1", "device": "/dev/vda"}]},
        {"id": "v2", "attachments": [{"server_id": "s2"}]} # Not attached to s1
    ]
    gb.link_server_volumes(server_id, volumes)
    
    edges = gb.graph.edges
    assert len(edges) == 1
    assert edges[0].from_node == "s1"
    assert edges[0].to_node == "volume:v1"
    assert edges[0].meta["device"] == "/dev/vda"
