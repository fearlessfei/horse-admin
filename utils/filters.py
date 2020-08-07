# -*- coding: utf-8 -*-

class ParamsQueryFilter:
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(**view.prune_query_params)
