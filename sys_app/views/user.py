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

    @HasPerm(perm_code='sys:user:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)

    @HasPerm(perm_code='sys:user:create')
    def create(self, request, *args, **kwargs):
        super(self.__class__, self).create(request, *args, **kwargs)

    @HasPerm(perm_code='sys:user:edit')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:user:delete')
    def destroy(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).destroy(request, pk, *args, **kwargs)
