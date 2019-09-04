# -*- coding: utf-8 -*-
from .base import AuthAPIViewSet
from utils.perm import HasPerm
from sys_app.serializers.menu import MenuSerializer
from sys_app.models import SYSMenu


class UserMenuViewSet(AuthAPIViewSet):
    """
    用户权限菜单
    """
    queryset = SYSMenu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        return queryset.filter(parent_id=0)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        menu_cond = dict(type__lt=2)

        if not request.user.is_superuser:
            user_id = request.user.id

            menu_id_list = []
            menu_objs = HasPerm().get_user_sidebar_menus(user_id)
            for menu_obj in menu_objs:
                menu_id_list.append(menu_obj.pk)

            queryset = queryset.filter(pk__in=menu_id_list)
            menu_cond = dict(pk__in=menu_id_list)

        serializer = self.get_serializer(
            instance=queryset,
            many=True,
            menu_cond=menu_cond
        )
        raise self.response.Success(data=serializer.data)
