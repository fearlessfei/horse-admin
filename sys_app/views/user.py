# *-* coding: utf-8 *-*
from django.contrib.auth import get_user_model

from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.user import UserSerializer

User = get_user_model()


class userViewSet(AuthAPIViewSet):
    """
    用户视图集
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        if not self.request.user.is_superuser:
            user_id = self.request.user.id
            queryset = queryset.filter(creator=user_id) | queryset.filter(id=user_id)
        return queryset

    @HasPerm(perm_code='sys:user:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)

    @HasPerm(perm_code='sys:user:create')
    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.data['is_superuser']:
            raise self.response.Fail(message="您不是超级管理员不能设置用户为超级管理员！")
        super(self.__class__, self).create(request, *args, **kwargs)

    @HasPerm(perm_code='sys:user:edit')
    def update(self, request, pk=None, *args, **kwargs):
        if not request.user.is_superuser:
            if request.data['is_superuser']:
                raise self.response.Fail(message="您不是超级管理员不能设置用户为超级管理员！")

            queryset = self.get_queryset()
            if not queryset.filter(id=pk):
                raise self.response.Fail(message="不能修改非自己创建的用户")

        super(self.__class__, self).update(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:user:delete')
    def destroy(self, request, pk=None, *args, **kwargs):
        if not request.user.is_superuser:
            queryset = self.get_queryset()
            if not queryset.filter(id=pk):
                raise self.response.Fail(message="不能删除非自己创建的用户")

        super(self.__class__, self).destroy(request, pk, *args, **kwargs)
