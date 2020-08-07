# *-* coding: utf-8 *-*
from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.group import GroupSerializer
from sys_app.models import SYSGroup


class GroupViewSet(AuthAPIViewSet):
    """
    组视图集
    """
    queryset = SYSGroup.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @HasPerm(perm_code='sys:group:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)

    @HasPerm(perm_code='sys:group:create')
    def create(self, request, *args, **kwargs):
        super(self.__class__, self).create(request, *args, **kwargs)

    @HasPerm(perm_code='sys:group:edit')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:group:delete')
    def destroy(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).destroy(request, pk, *args, **kwargs)
