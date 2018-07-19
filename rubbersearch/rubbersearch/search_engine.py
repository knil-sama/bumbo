import urllib.request
import typing as tp
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import dataclasses as dtc
from collections import Counter, defaultdict

@dtc.dataclass
class RequestInfo():
    """
    dataclass automatically create a __init__ and valid type for following atrributes
    """
    timestamp: int
    url: str

class SearchEngine:
    """
    This class will handle
        *fetching of dataset
        *parsing of dataset
        *storage of each datastructure used

    Notes:
        In later operations we will assume that content of dataset is already ordered by
    """
    data_pandas = None
    data_structure_hashmap = None
    data_structure_list = list()

    def __init__(self, file_url: str, file_dest :str="data.tsv.gz"):
        self._download_file(file_url, file_dest)
        res = pd.read_csv(file_dest,sep="\t", encoding='utf-8', names=["datetime_str", "url"])
        self._parse(res)

    def _download_file(self,url: str,file_dest: str):
        """
        Store dataset file in local filesystem

        Params:
            url(str): Remote location of file
            file_dest(str): Local path in filesystem

        """
        urllib.request.urlretrieve(url, file_dest) 

    def _parse(self,data: pd.DataFrame):
        """
        Load dataset in to the differents datastructure

        Params:
            data(pd.DataFrame): Content of the dataset
        """
        data["datetime"] = data["datetime_str"].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        data["timestamp"] = data["datetime"].map(lambda x: x.timestamp())
        data["request_info"] = data.apply(lambda row: RequestInfo(row["timestamp"], row["url"]), axis="columns")
        data["date"] = data["datetime"].map(lambda x: f'{x.year}-{x.month}-{x.day}')
        self.data_structure_hashmap = data.groupby("date")["request_info"].apply(lambda x: x.tolist()).to_dict()
        self.data_structure_list = data["request_info"].tolist()
        self.data_pandas = data


    def _query_parser(self, query: str) -> tp.Tuple[int, tp.Optional[int],  tp.Optional[int],  tp.Optional[int],
                                                    tp.Optional[int], dt.datetime, dt.datetime]:
        """
        Will format for different datastructure request, get str format as well a datetime range

        Params:
            query(str): Date prefix to parse

        Returns:
            int: Year
            tp.Optional[int]: Month
            tp.Optional[int]: Day
            hour(tp.Optional[int]: Hour
            tp.Optional[int]: Minute
            dt.datetime: Bottom window of date_prefix
            dt.datetime: Upper window of date_prefix
        """
        year = int(query[0:4])
        month = int(query[5:7]) if len(query) >= 7 else None
        day = int(query[8:10]) if len(query) >= 10 else None
        hour = int(query[11:13]) if len(query) >= 13 else None
        minute = int(query[14:16]) if len(query) >= 16 else None

        bottom_date = dt.datetime.strptime(f"{year}-{month if month else 1}-{ day if day else 1} { hour if hour else 0}:{minute if minute else 0}:00", "%Y-%m-%d %H:%M:%S")
        upper_date = dt.datetime.strptime(f"{year}-{month if month else 12}-{ day if day else 31} { hour if hour else 23}:{minute if minute else 59}:59", "%Y-%m-%d %H:%M:%S")
        # to getting correct calendar end of month
        if not day:
            upper_date += relativedelta(day=31)
        return year, month, day, bottom_date, upper_date,

    def _filtered_url_list(self, query: str) -> tp.Optional[tp.List[RequestInfo]]:
        """
        filter urls in datastructure_list based on date prefix

        Params:
            query(str): Date prefix of the query

        Returns:
             tp.Optional[tp.List[RequestInfo]]: Filter result on date prefix, None if not found
        """
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

    def _search_count_list(self,  query: str) -> int:
        """
        Count distinct urls for this query in datastructure list

        Params:
            query(str): Date prefix of the query

        Returns:
             int: Count of distinct value, 0 if None
        """
        filtered_urls = self._filtered_url_list(query)
        if filtered_urls:
            return len(set([value.url for value in filtered_urls]))
        else:
            return 0

    def _search_popular_list(self, query: str, size: int) -> list:
        """
        TopN of query based on datastructure list

        Params:
            query(str): Date prefix to filter on
            size(int): Number of element to return

        Returns:
            list: List of query ordered by descending value of total occurrence of url
        """
        filtered_urls = self._filtered_url_list(query)
        most_popular = Counter([value.url for value in filtered_urls]).most_common(size)
        formatted_result = [{ "query": result[0], "count": result[1]} for result in most_popular]
        return formatted_result

    def _search_count_pandas(self, query: str) -> int:
        """
        Count distinct urls for this query in datastructure pandas

        Params:
            query(str): Date prefix of the query

        Returns:
             int: Count of distinct value, 0 if None
        """
        _, _ , _, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp()
        return self.data_pandas[(self.data_pandas["timestamp"] >= bottom_window_timestamp) &  (self.data_pandas["timestamp"] <= upper_window_timestamp)]["url"].nunique(dropna=False)

    def _search_popular_pandas(self, query: str, size: int) -> list:
        """
        TopN of query based on datastructure pandas

        Params:
            query(str): Date prefix to filter on
            size(int): Number of element to return

        Returns:
            list: List of query ordered by descending value of total occurrence of url
        """
        _, _ , _, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp()
        list_filtered = self.data_pandas[(self.data_pandas["timestamp"] >= bottom_window_timestamp) &  (self.data_pandas["timestamp"] <= upper_window_timestamp)]["url"].tolist()
        most_popular = Counter(list_filtered).most_common(size)
        formatted_result = [{ "query": result[0], "count": result[1]} for result in most_popular]
        return formatted_result

    def _filtered_url_hashmap(self, query: str) -> tp.Optional[tp.List[RequestInfo]]:
        """
        filter urls in datastructure_hashmap based on date prefix

        Params:
            query(str): Date prefix of the query

        Returns:
             tp.Optional[tp.List[RequestInfo]]: Filter result on date prefix, None if not found
        """
        year, month, day, bottom_window, upper_window = self._query_parser(query)
        bottom_window_timestamp = bottom_window.timestamp()
        upper_window_timestamp = upper_window.timestamp()
        index_bottom =None
        index_upper =None
        url_of_the_day = self.data_structure_hashmap[f'{year}-{month}-{day}']
        for index, value in enumerate(url_of_the_day):
            if value.timestamp >= bottom_window_timestamp:
                index_bottom = index
                break
        if index_bottom is None:
            #nothing to found
            return None
        for index, value in enumerate(url_of_the_day[::-1]):
            if value.timestamp <= upper_window_timestamp:
                index_upper = len(url_of_the_day) - (index+1)
                break
        return url_of_the_day[index_bottom:index_upper]

    def _search_count_hashmap(self,  query: str) -> int:
        """
        Count distinct urls for this query in datastructure hashmap

        Params:
            query(str): Date prefix of the query

        Returns:
             int: Count of distinct value, 0 if None
        """
        filtered_urls = self._filtered_url_hashmap(query)
        if filtered_urls:
            return len(set([value.url for value in filtered_urls]))
        else:
            return 0

    def _search_popular_hashmap(self, query: str, size: int) -> list:
        """
        TopN of query based on datastructure hashmap

        Params:
            query(str): Date prefix to filter on
            size(int): Number of element to return

        Returns:
            list: List of query ordered by descending value of total occurrence of url
        """
        filtered_urls = self._filtered_url_hashmap(query)
        most_popular = Counter([value.url for value in filtered_urls]).most_common(size)
        formatted_result = [{ "query": result[0], "count": result[1]} for result in most_popular]
        return formatted_result
        
    def search_count(self, query: str, data_structure_choice: str) -> int:
        """

        Search distinct count, branch for corresponding datastructure

        Params:
            query(str): Raw query
            data_structure_choice(str): Datastructure name (either 'list','hashmap' or 'pandas')

        Returns:
            int: Number of distinct url for a time window, 0 if None
        """
        result = -1
        if(data_structure_choice == "hashmap"):
            result = self._search_count_hashmap(query)
        elif(data_structure_choice == "list"):
            result = self._search_count_list(query)
        elif(data_structure_choice == "pandas"):
            result = self._search_count_pandas(query)
        return result

    def search_popular(self, query: str, size: int, data_structure_choice: str) -> list:
        """

        Search distinct total count by branch, branch for corresponding datastructure

        Params:
            query(str): Raw query
            data_structure_choice(str): Datastructure name (either 'list','hashmap' or 'pandas')

        Returns:
            list: dict with the query as url value and count as total value
        """
        result = -1
        if(data_structure_choice == "hashmap"):
            result = self._search_popular_hashmap(query, size)
        elif(data_structure_choice == "list"):
            result = self._search_popular_list(query, size)
        elif(data_structure_choice == "pandas"):
            result = self._search_popular_pandas(query, size)
        return result