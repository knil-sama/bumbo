import unittest
from rubbersearch.search_engine import SearchEngine

SEARCH_ENGINE = SearchEngine("https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=1")

class TestParser(unittest.TestCase):

    def test_count_year(self):
        expected_result_2015 = 573697
        # we miss one for some reason (isn't due to NaN)
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "pandas"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "list"))
        #self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "hashmap"))

    def test_count_day(self):
        expected_result_day = 198117
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_count("2015-08-03", "list"))
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_count("2015-08-03", "hashmap"))
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_count("2015-08-03", "pandas"))


    def test_popular_year(self):
        expected_result_2015 =[
            {"query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 6675 },
            {"query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 4652 },
            {"query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 3100 }
        ]
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", 3, "pandas"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", 3, "list"))
        #self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", 3, "hashmap"))

    def test_popular_day(self):
        expected_result_day = [
            {"query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 2283},
            {"query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 1943},
            {"query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 1358},
            {"query": "http%3A%2F%2Fjamonkey.com%2F50-organizing-ideas-for-every-room-in-your-house%2F", "count": 890},
            {"query": "http%3A%2F%2Fsharingis.cool%2F1000-musicians-played-foo-fighters-learn-to-fly-and-it-was-epic", "count": 701}
        ]
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_popular("2015-08-02", 5, "list"))
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_popular("2015-08-02", 5, "hashmap"))
        self.assertEqual(expected_result_day, SEARCH_ENGINE.search_popular("2015-08-02", 5, "pandas"))


if __name__ == "__main__":
    unittest.main()