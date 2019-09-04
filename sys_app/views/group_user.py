# *-* coding: utf-8 *-*
from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.group_user import GroupUserSerializer
from sys_app.models import SYSGroup


class GroupUserViewSet(AuthAPIViewSet):
    """
    组用户视图集
    """
    queryset = SYSGroup.objects.all()
    serializer_class = GroupUserSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).retrieve(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:group:user')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)
