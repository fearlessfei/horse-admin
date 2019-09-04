# *-* coding: utf-8 *-*
from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.role_menu import RoleMenuSerializer
from sys_app.models import SYSRole


class RoleMenuViewSet(AuthAPIViewSet):
    """
    角色菜单视图集
    """
    queryset = SYSRole.objects.all()
    serializer_class = RoleMenuSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).retrieve(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:role:perm')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)
