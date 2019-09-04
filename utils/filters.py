# -*- coding: utf-8 -*-

class ParamsQueryFilter:
    def filter_queryset(self, request, queryset, view):
        cond = dict()

        query_params = view.prune_query_params
        for param in query_params:
                cond[param+'__contains'] = query_params[param]
        print('query_cond: ', cond)
        queryset = queryset.filter(**cond)

        return queryset