import falcon

VERSION = 1
API = "queries"

class CountResource:
    def on_get(self, req, resp, date_prefix):
        """Handles GET requests"""
        result = { count: 573697 }
        resp.media = result
def create():
    api = falcon.API()
    api.add_route(f'/{VERSION}/{API}/count/{{date_prefix}}', CountResource())
    return api

if __name__ == '__main__':
    app = create()
    httpd = simple_server.make_server('', 8000, app)
    httpd.serve_forever()
