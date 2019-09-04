# *-* coding: utf-8 *-*
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils import exceptions
from utils.filters import ParamsQueryFilter


class BaseViewSet(viewsets.ModelViewSet):
    """
    基本视图集
    """
    response = exceptions

    filter_backends = (ParamsQueryFilter, )

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                raise self.response.PermissionDenied()

    @property
    def prune_query_params(self):
        """
        精简过的查询参数
        :return:
        """
        params = {}

        query_params = self.request.query_params
        for k in query_params:
            if k not in ['page', 'limit'] and query_params[k]:
                params[k] = query_params[k]
        return params

    def get_object(self):

        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        print('lookup_field: ', self.lookup_field)
        print('kwargs: ', self.kwargs)
        obj = queryset.filter(**filter_kwargs).first()
        if not obj:
            self.response.Fail(message='记录不存在')

        self.check_object_permissions(self.request, obj)

        return obj

    def check_pk_is_exist(self, pk_value, pk_attr='pk'):
        """
        检查主键是否存在
        :param pk_value: 主键值
        :param pk_attr: 主键属性，默认为pk
        :return:
        """
        print(pk_attr, pk_value)
        queryset = self.get_queryset().filter(**{pk_attr: pk_value})
        if not queryset.exists():
            self.response.Fail(message='记录不存在')

    def is_valid(self, serializer):
        """
        数据是否验证通过
        :param serializer:
        :return:
        """
        if not serializer.is_valid():
            message = ''
            errors = serializer.errors
            print(errors)
            for field in errors:
                message += str(errors[field][0])+'\n'
            raise self.response.Fail(message=message)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        pg_queryset = self.paginate_queryset(queryset=queryset)
        query_params = self.request.query_params
        # 不分页
        if 'page' not in query_params and 'limit' not in query_params:
            pg_queryset = None

        if pg_queryset is not None:
            serializer = self.get_serializer(instance=pg_queryset, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            data = self.get_serializer(instance=queryset, many=True).data
        print('List data: ', data)
        raise self.response.Success(data=data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        self.check_pk_is_exist(pk)

        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        print('Retrieve data: ', serializer.data)
        raise self.response.Success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        self.is_valid(serializer)
        self.perform_create(serializer)

        raise self.response.Success()

    def update(self, request, pk=None, *args, **kwargs):
        self.check_pk_is_exist(pk)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        self.is_valid(serializer)
        self.perform_update(serializer)

        raise self.response.Success()

    def destroy(self, request, pk=None, *args, **kwargs):
        self.check_pk_is_exist(pk)

        rows, _ = self.get_queryset().filter(pk=pk).delete()
        if rows > 0:
            raise self.response.Success()
        raise self.response.Fail()


class AuthAPIViewSet(BaseViewSet):
    """
    带认证的视图集
    """
    authentication_classes = (JSONWebTokenAuthentication, )
