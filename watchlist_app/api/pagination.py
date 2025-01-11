from rest_framework.pagination import PageNumberPagination


# define your custom pagination classes here

class WatchListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'    # default is 'page'
    page_size_query_param = 'size'    # this query parameter can be used by user to get custom number of data
    max_page_size = 10
    last_page_strings = ('end',)    # a list or tuple of string values indicating values that may be used with the page_query_param to request the final page in the set
