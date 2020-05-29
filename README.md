# NeoLite

Super light weight neo4j python driver with **multi-graph** support.

## Installation

```bash
pip install neolite
```

## Basic Example

```python
from neolite import Graph

graph = Graph(host, auth=(username, password), db=db)

result = graph.cypher('''
    CREATE ( bike:Bike { weight: 10 } ) 
    CREATE ( frontWheel:Wheel { spokes: 3 } ) 
    CREATE ( backWheel:Wheel { spokes: 32 } ) 
    CREATE p1 = (bike)-[:HAS { position: 1 } ]->(frontWheel) 
    CREATE p2 = (bike)-[:HAS { position: 2 } ]->(backWheel) 
    RETURN bike, p1, p2
''')
print(result)
```

## Advanced Usage

### Show execution stats

```python
result = graph.cypher('SOME CYPHER', stat=True)
```

### Multiple commits in at the same time

```python
result = graph.cypher_many([
    'SOME CYPHER',
    'ANOTHER CYPHER'
])
```

### Get table-like results instead of graph-like ones

```python
result = graph.cypher('SOME CYPHER', ret_type='table')
```

### Use https over http

```python
graph = Graph(host, encrypted=True)
```
