# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页
    """
    #每页显示多少个
    page_size = 1
    #默认每页显示20个，可以通过传入xxx/?page=2&limit=4,改变默认每页显示的个数
    page_size_query_param = "limit"
    #最大不超过多少页数，这里设置None无限制
    max_page_size = None
    #获取页码数参数
    page_query_param = "page"

    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'results': data
        }