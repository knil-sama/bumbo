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
    def test_get_message(self):
        doc = { "count": 573697 }

        result = self.simulate_get('/1/queries/count/2015')
        self.assertEqual(result.json, doc)
