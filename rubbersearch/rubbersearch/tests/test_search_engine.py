import unittest
from rubbersearch.search_engine import SearchEngine

SEARCH_ENGINE = SearchEngine("https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=1")

class TestParser(unittest.TestCase):

    def test_test_count_year_perf(self):
        expected_result_2015 = 573697
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "pandas"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "list"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_count("2015", "hashmap"))

    def test_test_popular_year_perf(self):
        expected_result_2015 =[
            { "query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 6675 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 4652 },
            { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 3100 }
        ]
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", "pandas"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", "list"))
        self.assertEqual(expected_result_2015, SEARCH_ENGINE.search_popular("2015", "hashmap"))

if __name__ == "__main__":
    unittest.main()