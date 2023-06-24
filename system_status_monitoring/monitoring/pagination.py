from rest_framework.pagination import PageNumberPagination

class SystemInfoPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'system-page'
    page_size_query_param = 'system-size'
    max_page_size = 99


class SystemInfoListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'system-page'
    page_size_query_param = 'system-size'
    max_page_size = 99

