import urllib.request
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import dataclasses as dtc
from collections import Counter

@dtc.dataclass
class RequestInfo():
    timestamp: int
    url: str

class SearchEngine(object):
    data_pandas = None
    data_structure_hashmap = dict()
    # assume that logs are ordered be ascending timestamp
    data_structure_list = list()

    def __init__(self, file_url: str, file_dest :str="data.tsv.gz"):
        self._download_file(file_url, file_dest)
        res = pd.read_csv(file_dest,sep="\t", encoding='utf-8', names=["datetime_str", "url"])
        self._parse(res)

    def _download_file(self,url: str,file_dest: str):
        urllib.request.urlretrieve(url, file_dest) 

    def _parse(self,data: pd.DataFrame):
        data["datetime"] = data["datetime_str"].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        data["timestamp"] = data["datetime"].map(lambda x: x.timestamp())
        data["request_info"] = data.apply(lambda row: RequestInfo(row["timestamp"], row["url"]), axis="columns")
        self.data_pandas = data
        self.data_structure_list = data["request_info"].tolist()
        #data.apply(lambda row, data_structure=self.data_structure_hashmap:
        # data_structure.get(row["datetime"].year, dict())
        # .get(row["datetime"].month, dict())
        # .get(row["datetime"].day, list()).append(row["request_info"]), axis="columns")

    def _query_parser(self, query):
        """
        Will format for different datastructure request, get str format as well a datetime range
        """
        year = query[0:4]
        month = query[5:7] if len(query) > 7 else None
        day = query[8:10] if len(query) > 10 else None
        hour = query[11:13] if len(query) > 13 else None
        minute = query[14:16] if len(query) > 16 else None

        bottom_date = dt.datetime.strptime(f"{year}-{month if month else 1}-{ day if day else 1} { hour if hour else 0}:{minute if minute else 0}:00", "%Y-%m-%d %H:%M:%S")
        upper_date = dt.datetime.strptime(f"{year}-{month if month else 12}-{ day if day else 1} { hour if hour else 23}:{minute if minute else 59}:59", "%Y-%m-%d %H:%M:%S")
        #to getting correct calendar end of month
        if not day:
            upper_date +=relativedelta(day=31) 
        return year, month, day, bottom_date, upper_date, 

    def _filtered_url_list(self, query: str):
        _, _, _, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp() 
        index_bottom =None
        index_upper =None
        for index, value in enumerate(self.data_structure_list):
            if value.timestamp >= bottom_window_timestamp:
                index_bottom = index
                break
        if index_bottom is None:
            #nothing to found
            return None
        for index, value in enumerate(self.data_structure_list[::-1]):
            if value.timestamp <= upper_window_timestamp:
                index_upper = len(self.data_structure_list) - (index+1)
                break
        return self.data_structure_list[index_bottom:index_upper]

    def _search_count_list(self,  query: str):
        filtered_urls = self._filtered_url_list(query)
        if filtered_urls:
            return len(set([value.url for value in filtered_urls]))
        else:
            return 0

    def _search_popular_list(self, query: str, size: int):
        filtered_urls = self._filtered_url_list(query)
        most_popular = Counter([value.url for value in filtered_urls]).most_common(size)
        formatted_result = [{ "query": result[0], "count": result[1]} for result in most_popular]
        return formatted_result

    def _search_count_pandas(self, query: str):
        _, _ , _, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp()
        return self.data_pandas[(self.data_pandas["timestamp"] >= bottom_window_timestamp) &  (self.data_pandas["timestamp"] <= upper_window_timestamp)]["url"].nunique(dropna=False)

    def _search_popular_pandas(self, query: str, size: int):
        _, _ , _, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp()
        list_filtered = self.data_pandas[(self.data_pandas["timestamp"] >= bottom_window_timestamp) &  (self.data_pandas["timestamp"] <= upper_window_timestamp)]["url"].tolist()
        most_popular = Counter(list_filtered).most_common(size)
        formatted_result = [{ "query": result[0], "count": result[1]} for result in most_popular]
        return formatted_result

    def _search_popular_hashmap(self,  query: str, size: int):
        return []
        
    def search_count(self, query: str, data_structure_choice: str):
        result = -1
        if(data_structure_choice == "hashmap"):
            pass
            # make computer crash now :( result = self._search_count_hashmap(query)
        elif(data_structure_choice == "list"):
            result = self._search_count_list(query)
        elif(data_structure_choice == "pandas"):
            result = self._search_count_pandas(query)
        return result

    def search_popular(self, query: str, size: int, data_structure_choice: str):
        result = -1
        if(data_structure_choice == "hashmap"):
            result = self._search_popular_hashmap(query, size)
        elif(data_structure_choice == "list"):
            result = self._search_popular_list(query, size)
        elif(data_structure_choice == "pandas"):
            result = self._search_popular_pandas(query, size)
        return result

if __name__ == '__main__':
    search_engine = SearchEngine("https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=1")
    # print(search_engine)
    print(search_engine.data_pandas.head())
    print(search_engine.search_count("2015", "list"))