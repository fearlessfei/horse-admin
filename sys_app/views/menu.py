# *-* coding: utf-8 *-*
from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.menu import MenuSerializer
from sys_app.models import SYSMenu


class MenuViewSet(AuthAPIViewSet):
    """
    菜单视图集
    """
    queryset = SYSMenu.objects.all()
    serializer_class = MenuSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        if self.action == 'list':
            if not self.prune_query_params:
                return queryset.filter(parent_id=0)
        return queryset

    @HasPerm(perm_code='sys:menu:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)

    @HasPerm(perm_code='sys:menu:create')
    def create(self, request, *args, **kwargs):
        super(self.__class__, self).create(request, *args, **kwargs)

    @HasPerm(perm_code='sys:menu:edit')
    def update(self, request, pk=None, *args, **kwargs):
        super(self.__class__, self).update(request, pk, *args, **kwargs)

    @HasPerm(perm_code='sys:menu:delete')
    def destroy(self, request, pk=None, *args, **kwargs):
        # 首先把要删除的菜单本身添加到列表
        menu_id_list = [pk]
        # 获取到所有子菜单
        def get_child_menu_id_list(menu_objs):
            for menu_obj in menu_objs:
                _menu_id = menu_obj.id
                menu_id_list.append(_menu_id)

                _menu_objs = SYSMenu.objects.filter(parent_id=_menu_id)
                if _menu_objs:
                    get_child_menu_id_list(_menu_objs)

        menu_objs = SYSMenu.objects.filter(parent_id=pk)
        get_child_menu_id_list(menu_objs)
        rows, _ = SYSMenu.objects.filter(id__in=menu_id_list).delete()
        if rows > 0:
            raise self.response.Success()
        raise self.response.Fail()
