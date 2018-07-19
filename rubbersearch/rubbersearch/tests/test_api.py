from falcon import testing
from rubbersearch import app

class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = app.create()


class TestApi(MyTestCase):
    def test_get_call_count_year(self):
        doc = { "count": 573697 }

        result = self.simulate_get('/1/queries/count/2015')
        self.assertEqual(result.json, doc)

    def test_get_call_count_day(self):
        doc = { "count": 198117 }

        result = self.simulate_get('/1/queries/count/2015-08-03')
        self.assertEqual(result.json, doc)

    def test_get_call_popular_year(self):
        doc = { "queries": [
            { "query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 6675 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 4652 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 3100 }
            ]
        }
        result = self.simulate_get('/1/queries/popular' ,query_string='date_prefix=2015&size=3')
        self.assertEqual(result.json, doc)

    def test_get_call_popular_day(self):
        doc = { "queries": [
            { "query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 2283 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 1943 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 1358 },
            { "query": "http%3A%2F%2Fjamonkey.com%2F50-organizing-ideas-for-every-room-in-your-house%2F", "count": 890 },
            { "query": "http%3A%2F%2Fsharingis.cool%2F1000-musicians-played-foo-fighters-learn-to-fly-and-it-was-epic", "count": 701 }
            ]
        }
        self.maxDiff = None
        result = self.simulate_get('/1/queries/popular', query_string='date_prefix=2015-08-02&size=5')
        self.assertEqual(result.json, doc)
