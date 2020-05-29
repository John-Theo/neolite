from credentials import host, username, password, db
from neolite import Graph, CypherError
import pytest


@pytest.fixture
def auth_graph():
    graph = Graph(host, auth=(username, password), db=db)
    graph.server_info()
    return graph


@pytest.fixture
def no_auth_graph():
    graph = Graph('localhost')
    graph.server_info()
    return graph


def test_auth(auth_graph):
    result = auth_graph.cypher('''
        CREATE ( bike:Bike { weight: 10 } ) 
        CREATE ( frontWheel:Wheel { spokes: 3 } ) 
        CREATE ( backWheel:Wheel { spokes: 32 } ) 
        CREATE p1 = (bike)-[:HAS { position: 1 } ]->(frontWheel) 
        CREATE p2 = (bike)-[:HAS { position: 2 } ]->(backWheel) 
        RETURN bike, p1, p2
    ''', stats=True)
    assert result
    assert set(result.keys()) == {'nodes', 'relationships'}
    assert set(result['nodes'][0].keys()) == {'id', 'labels', 'properties'}
    assert set(result['relationships'][0].keys()) == {'id', 'type', 'properties', 'startNode', 'endNode'}


def test_no_auth(no_auth_graph):
    result = no_auth_graph.cypher('''
        CREATE ( bike:Bike { weight: 10 } ) 
        CREATE ( frontWheel:Wheel { spokes: 3 } ) 
        CREATE ( backWheel:Wheel { spokes: 32 } ) 
        CREATE p1 = (bike)-[:HAS { position: 1 } ]->(frontWheel) 
        CREATE p2 = (bike)-[:HAS { position: 2 } ]->(backWheel) 
        RETURN bike, p1, p2
    ''', stats=True)
    assert result
    assert set(result.keys()) == {'nodes', 'relationships'}
    assert set(result['nodes'][0].keys()) == {'id', 'labels', 'properties'}
    assert set(result['relationships'][0].keys()) == {'id', 'type', 'properties', 'startNode', 'endNode'}


def test_wrong_cypher(no_auth_graph):
    with pytest.raises(CypherError) as excinfo:
        result = no_auth_graph.cypher('''
            RETURN a
        ''', stats=True)
        assert 'Neo.ClientError.Statement.SyntaxError' in str(excinfo.value)
