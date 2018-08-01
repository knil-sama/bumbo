import falcon
import json
from wsgiref import simple_server

from rubbersearch import SEARCH_ENGINE

VERSION = 1
API = "queries"

class CountResource:
    """
    Rest API resource for count endpoint
    """
    def on_get(self, _req, resp, date_prefix):
        """Handles GET requests"

        Count distinct url for a delimited time period

        Args:
            _req: Request content
            resp: Response to return
            date_prefix(str): Date that delimit window a time for count
        """
        #small optimisation for date_prefix that have a day scope
        if len(date_prefix) >= 10:
            result = { "count": SEARCH_ENGINE.search_count(date_prefix, "hashmap") }
        else:
            result = { "count": SEARCH_ENGINE.search_count(date_prefix, "list") }
        resp.body = json.dumps(result)

class PopularResource:
    """
    Rest API resource for popular endpoint
    """
    def on_get(self, req, resp, date_prefix):
        """Handles GET requests

        Top n with count of total queries for a delimited time period, in descending order

        Args:
            req: Request content
            resp: Response to return
        """
        #small optimisation for date_prefix that have a day scope
        size = req.get_param_as_int('size') or 5
        if len(date_prefix) >= 10:
            result = { "queries": SEARCH_ENGINE.search_popular(date_prefix, size, "hashmap") }
        else:
            result = { "queries": SEARCH_ENGINE.search_popular(date_prefix, size,"list") }
        resp.body = json.dumps(result)

def create():
    """
    Create and api and setup route

    Returns:
         falcon.API: api ready to be launched
    """
    api = falcon.API()
    api.add_route(f'/{VERSION}/{API}/count/{{date_prefix}}', CountResource())
    api.add_route(f'/{VERSION}/{API}/popular/{{date_prefix}}', PopularResource())
    return api

if __name__ == '__main__':
    app = create()
    httpd = simple_server.make_server('', 8000, app)
    httpd.serve_forever()
