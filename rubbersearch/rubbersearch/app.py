import falcon
from rubbersearch.search_engine import SearchEngine
VERSION = 1
API = "queries"

SEARCH_ENGINE = SearchEngine("https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=1")

class CountResource:
    def on_get(self, req, resp, date_prefix):
        """Handles GET requests"""
        result = { "count": SEARCH_ENGINE.search_count(req, "pandas") }
        resp.media = result


def create():
    api = falcon.API()
    api.add_route(f'/{VERSION}/{API}/count/{{date_prefix}}', CountResource())
    return api

if __name__ == '__main__':
    app = create()
    httpd = simple_server.make_server('', 8000, app)
    httpd.serve_forever()
