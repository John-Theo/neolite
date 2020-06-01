import requests
from pprint import pformat, pprint


class CypherError(SyntaxError):
    pass


class Graph:
    def __init__(self, host, port=7474, db='neo4j', auth=None, encrypted=False):
        auth = f'{auth[0]}:{auth[1]}@' if auth else ''
        protocol = 'https' if encrypted else 'http'
        self.uri = f'{protocol}://{host}:{port}'
        self.commit_uri = f'{protocol}://{auth}{host}:{port}/db/{db}/tx/commit'
        assert self._server_info()

    def _server_info(self):
        return requests.get(self.uri).json()
    
    def server_info(self):
        pprint(self._server_info())

    def cypher_many(self, statements, ret_type='graph', stats=False):
        """
        statement: (<list>, <tuple>)
        ret_type: ('table', 'graph')
        """
        assert ret_type in ('table', 'graph')
        assert any([isinstance(statements, x) for x in (list, tuple)])
        data = "row" if ret_type == 'table' else 'graph'
        resp = requests.post(self.commit_uri, json={
            "statements": [{
                "statement": s.strip(),
                "includeStats": True,
                "resultDataContents": [data]
            } for s in statements]
        }).json()
        if resp['errors']:
            error = resp['errors'][0]
            raise CypherError(f'\n{error["code"]}: {error["message"]}')
        return [self.format(c.strip(), r, ret_type, stats) for c, r in zip(
            statements, resp['results']
        )]

    @staticmethod
    def format(cypher, raw, ret_type, show_stats):
        stats = {
            'cypher': cypher,
            **{k: v for k, v in raw['stats'].items() if v}
        }
        if show_stats:
            pprint(stats)
        if not raw['data']:
            return None
        if ret_type == 'table':
            return {'columns': raw['columns'], **raw['data'][0]}
        else:
            return raw['data'][0]['graph']

    def cypher(self, statement, ret_type='graph', stats=False):
        return self.cypher_many([statement], ret_type, stats)[0]


if __name__ == "__main__":
    Graph('localhost').cypher('CREATE(a) RETURN a')