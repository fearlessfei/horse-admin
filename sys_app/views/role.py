# *-* coding: utf-8 *-*
from django.contrib.auth import get_user_model

from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.role import RoleSerializer
from sys_app.models import SYSRole

User = get_user_model()


class RoleViewSet(AuthAPIViewSet):
    """
    角色视图集
    """
    queryset = SYSRole.objects.all()
    serializer_class = RoleSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @HasPerm(perm_code='sys:role:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)

    @HasPerm(perm_code='sys:role:create')
    def create(self, request, *args, **kwargs):
        super(self.__class__, self).create(request, *args, **kwargs)

    @HasPerm(perm_code='sys:role:edit')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:role:delete')
    def destroy(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).destroy(request, pk, *args, **kwargs)
