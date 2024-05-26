from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)


class ProductListPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 50
    
    
class ProductListOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10