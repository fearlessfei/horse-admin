# *-* coding: utf-8 *-*
from functools import wraps
from itertools import chain

from rest_framework.permissions import BasePermission

from utils.exceptions import PermissionDenied
from sys_app.serializers.menu import MenuType
from sys_app.models import (
    SYSGroupUser,
    SYSGroupRole,
    SYSRoleMenu,
    SYSUserRole,
)


class HasPerm(object):
    def __init__(self, perm_code=""):
        self.perm_code = perm_code

    def get_user_groups(self, user_id):
        """
        获取用户组
        :param user_id:
        :return:
        """
        user_group_objs = SYSGroupUser.objects.filter(user_id=user_id)
        return user_group_objs

    def get_group_roles(self, group_id_list=None):
        """
        获取组角色
        :param group_id_list:
        :return:
        """
        if group_id_list is None:
            group_id_list = []

        group_role_objs = SYSGroupRole.objects.filter(group_id__in=group_id_list)
        return group_role_objs

    def get_user_role(self, user_id):
        """
        获取用户角色
        :param user_id:
        :return:
        """
        user_role_objs = SYSUserRole.objects.filter(user_id=user_id)
        return user_role_objs

    def get_role_menus(self, role_id_list=None):
        """
        获取角色菜单
        :param role_id_list:
        :return:
        """
        if role_id_list is None:
            role_id_list = []

        role_menu_objs = SYSRoleMenu.objects.filter(role_id__in=role_id_list)
        return role_menu_objs

    def get_user_menus(self, user_id):
        """
        获取用户拥有的菜单
        :param user_id:
        :return:
        """
        menu_objs = []
        role_objs = []

        user_group_objs = self.get_user_groups(user_id)
        if user_group_objs:
            group_id_list = [user_group_obj.group for user_group_obj in user_group_objs]
            role_objs = self.get_group_roles(group_id_list)

        # 如果用户所在组没有权限继续判断用户所有拥护的权限,删除重复的权限
        role_objs = chain(role_objs, (self.get_user_role(user_id)))

        # 用户不属于任何角色的情况
        if not role_objs:
            return menu_objs

        role_id_list = [role_obj.role_id for role_obj in role_objs]
        role_id_list = list(set(role_id_list))
        role_menu_objs = self.get_role_menus(role_id_list)

        # 角色没有被分配权限的情况
        if not role_menu_objs:
            return menu_objs

        menu_objs = [perm_menu_obj.menu for perm_menu_obj in role_menu_objs]
        return menu_objs

    def get_user_sidebar_menus(self, user_id):
        """
        获取用户侧边栏菜单
        :param user_id:
        :return:
        """
        menu_objs = []

        _menu_objs = self.get_user_menus(user_id)
        for menu_obj in _menu_objs:
            if menu_obj.type < MenuType.BUTTON:
                menu_objs.append(menu_obj)

        return menu_objs

    def get_user_perm_code_list(self, user_id):
        """
        获取用户拥有的权限
        :param user_id:
        :return:
        """
        perm_code_list = []

        menu_objs = self.get_user_menus(user_id)
        for menu_obj in menu_objs:
            if menu_obj.type == MenuType.BUTTON:
                if menu_obj.perm_code not in perm_code_list:
                    perm_code_list.append(menu_obj.perm_code)

        return perm_code_list

    def is_has_perm(self, user_id, perm_code):
        """
        是否有权限
        :param user_id: 用户ID
        :param perm_code: 权限代码
        :return:
        """
        return perm_code in self.get_user_perm_code_list(user_id)

    def __call__(self, func, *args, **kwargs):
        self.func = func

        @wraps(self.func)
        def perm_wrraper(_self, request, *args, **kwargs):
            is_superuser = request.user.is_superuser
            if is_superuser:
                self.func(_self, request, *args, **kwargs)
                return

            user_id = request.user.id
            if not self.is_has_perm(user_id, self.perm_code):
                raise PermissionDenied(message="您没有操作权限")
            self.func(_self, request, *args, **kwargs)

        return perm_wrraper


class IsSuperUser(BasePermission):
    """
    只允许超级管理员访问
    """
    def has_permission(self, request, view):
        if not request.user and request.user.is_superuser:
            raise view.response.PermissionDenied(message="只允许超级管理员操作")
        return True


class IsOwner(BasePermission):
    """
    只允许所有者访问
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.id == obj.id:
            return True
        raise view.response.PermissionDenied(message="只允许操作自己的信息")
