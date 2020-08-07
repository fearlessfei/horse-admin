# *-* coding: utf-8 *-*
from rest_framework import viewsets
from rest_framework_mongoengine import viewsets as Mongoviewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils import exceptions
from utils.filters import ParamsQueryFilter


class ViewSetMixin:
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
            raise self.response.Fail(message='记录不存在')

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
            raise self.response.Fail(message='记录不存在')

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

    def before_list_return(self, data):
        #extra handle before return data
        return data
    
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
        
        data = self.before_list_return(data)
        print('List data: ', data)
        raise self.response.Success(data=data)

    def before_retrieve_return(self, data):
        #extra handle before return data
        return data
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        data = serializer.data
        data = self.before_retrieve_return(data)
        print('Retrieve data: ', data)
        raise self.response.Success(data=data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        self.is_valid(serializer)
        self.perform_create(serializer)

        raise self.response.Success()

    def update(self, request, pk=None, *args, **kwargs):
        self.check_pk_is_exist(pk)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        self.is_valid(serializer)
        self.perform_update(serializer)

        raise self.response.Success()

    def destroy(self, request, pk=None, *args, **kwargs):
        self.check_pk_is_exist(pk)

        rows, _ = self.get_queryset().filter(pk=pk).delete()
        if rows > 0:
            raise self.response.Success()
        raise self.response.Fail()

    def condition_destroy(self, request, pk=None, delete_key='is_delete', *args, **kwargs):
        """条件删除"""
        self.check_pk_is_exist(pk)

        rows = self.get_queryset().filter(pk=pk).update(**{delete_key: 1})
        if rows > 0:
            raise self.response.Success()
        raise self.response.Fail()

    def get_delete_ids(self, request):
        """获取批量删除id"""
        delete_ids = request.data.get('delete_ids', None)

        if not delete_ids:
            raise self.response.Fail()

        return [int(_id.strip()) for _id in delete_ids.split(',')]

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        """批量删除"""
        btn_ids = self.get_delete_ids(request)
        self.get_queryset().filter(id__in=btn_ids).delete()
        raise self.response.Success()

    def condtion_multiple_delete(self, request, delete_key='is_delete', *args, **kwargs):
        """条件批量删除"""
        btn_ids = self.get_delete_ids(request)
        rows = self.get_queryset().filter(id__in=btn_ids).update(**{delete_key: 1})
        if rows > 0:
            raise self.response.Success()
        raise self.response.Fail()


class MongoAuthAPIViewSet(ViewSetMixin, Mongoviewsets.ModelViewSet):
    """
    带认证的视图集
    """
    authentication_classes = (JSONWebTokenAuthentication, )


class AuthAPIViewSet(ViewSetMixin, viewsets.ModelViewSet):
    """
    带认证的视图集
    """
    authentication_classes = (JSONWebTokenAuthentication, )


class BaseAPIView(APIView):
    """
    基本视图
    """
    response = exceptions


class AuthAPIView(BaseAPIView):
    """
    带认证的视图
    """
    authentication_classes = (JSONWebTokenAuthentication, )
