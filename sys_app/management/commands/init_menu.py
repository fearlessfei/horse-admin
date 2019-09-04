# *-* coding: utf-8 *-*
import traceback

from sys_app.models import SYSMenu
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        menu_list = [
            {
                "id": 1,
                "parent_id": 0,
                "path": "/sys",
                "component": "index",
                "redirect": "/",
                "name": "sys",
                "title": "系统管理",
                "icon": "sys",
                "type": 0,
                "perm_code": "",
                "creator_id": 1
            },
            {
                "id": 2,
                "parent_id": 1,
                "path": "user",
                "component": "sys/user/index",
                "redirect": "",
                "name": "sys_user",
                "title": "用户管理",
                "icon": "user",
                "type": 1,
                "perm_code": "",
                "creator_id": 1
            },
            {
                "id": 3,
                "parent_id": 1,
                "path": "role",
                "component": "sys/role/index",
                "redirect": "",
                "name": "sys_role",
                "title": "角色管理",
                "icon": "role",
                "type": 1,
                "perm_code": "",
                "creator_id": 1
            },
            {
                "id": 4,
                "parent_id": 1,
                "path": "menu",
                "component": "sys/menu/index",
                "redirect": "",
                "name": "sys_menu",
                "title": "菜单管理",
                "icon": "nested",
                "type": 1,
                "perm_code": "",
                "creator_id": 1
            },
            {
                "id": 5,
                "parent_id": 1,
                "path": "group",
                "component": "sys/group/index",
                "redirect": "",
                "name": "sys_group",
                "title": "用户组管理",
                "icon": "group",
                "type": 1,
                "perm_code": "",
                "creator_id": 1
            },
            {
                "id": 6,
                "parent_id": 3,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_role_edit",
                "title": "编辑",
                "icon": "edit",
                "type": 2,
                "perm_code": "sys:role:edit",
                "creator_id": 1
            },
            {
                "id": 7,
                "parent_id": 3,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_role_delete",
                "title": "删除",
                "icon": "delete",
                "type": 2,
                "perm_code": "sys:role:delete",
                "creator_id": 1
            },
            {
                "id": 8,
                "parent_id": 3,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_role_select",
                "title": "查询",
                "icon": "select",
                "type": 2,
                "perm_code": "sys:role:select",
                "creator_id": 1
            },
            {
                "id": 9,
                "parent_id": 3,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_role_create",
                "title": "创建",
                "icon": "create",
                "type": 2,
                "perm_code": "sys:role:create",
                "creator_id": 1
            },
            {
                "id": 10,
                "parent_id": 3,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_role_perm",
                "title": "权限",
                "icon": "perm",
                "type": 2,
                "perm_code": "sys:role:perm",
                "creator_id": 1
            },
            {
                "id": 11,
                "parent_id": 2,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_user_create",
                "title": "创建",
                "icon": "create",
                "type": 2,
                "perm_code": "sys:user:create",
                "creator_id": 1
            },
            {
                "id": 12,
                "parent_id": 2,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_user_select",
                "title": "查询",
                "icon": "select",
                "type": 2,
                "perm_code": "sys:user:select",
                "creator_id": 1
            },
            {
                "id": 13,
                "parent_id": 2,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_user_edit",
                "title": "编辑",
                "icon": "edit",
                "type": 2,
                "perm_code": "sys:user:edit",
                "creator_id": 1
            },
            {
                "id": 14,
                "parent_id": 2,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_user_delete",
                "title": "删除",
                "icon": "delete",
                "type": 2,
                "perm_code": "sys:user:delete",
                "creator_id": 1
            },
            {
                "id": 15,
                "parent_id": 4,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_menu_select",
                "title": "查询",
                "icon": "select",
                "type": 2,
                "perm_code": "sys:menu:select",
                "creator_id": 1
            },
            {
                "id": 16,
                "parent_id": 4,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_menu_create",
                "title": "创建",
                "icon": "create",
                "type": 2,
                "perm_code": "sys:menu:create",
                "creator_id": 1
            },
            {
                "id": 17,
                "parent_id": 4,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_menu_edit",
                "title": "编辑",
                "icon": "edit",
                "type": 2,
                "perm_code": "sys:menu:edit",
                "creator_id": 1
            },
            {
                "id": 18,
                "parent_id": 4,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_menu_delete",
                "title": "删除",
                "icon": "delete",
                "type": 2,
                "perm_code": "sys:menu:delete",
                "creator_id": 1
            },
            {
                "id": 19,
                "parent_id": 5,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_group_select",
                "title": "查询",
                "icon": "select",
                "type": 2,
                "perm_code": "sys:group:select",
                "creator_id": 1
            },
            {
                "id": 20,
                "parent_id": 5,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_group_create",
                "title": "创建",
                "icon": "create",
                "type": 2,
                "perm_code": "sys:group:create",
                "creator_id": 1
            },
            {
                "id": 21,
                "parent_id": 5,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_group_edit",
                "title": "编辑",
                "icon": "edit",
                "type": 2,
                "perm_code": "sys:group:edit",
                "creator_id": 1
            },
            {
                "id": 22,
                "parent_id": 5,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_group_delete",
                "title": "删除",
                "icon": "delete",
                "type": 2,
                "perm_code": "sys:group:delete",
                "creator_id": 1
            },
            {
                "id": 23,
                "parent_id": 5,
                "path": "",
                "component": "",
                "redirect": "",
                "name": "sys_group_user",
                "title": "用户",
                "icon": "perm",
                "type": 2,
                "perm_code": "sys:group:user",
                "creator_id": 1
            }
        ]
        try:
            if SYSMenu.objects.filter():
                print("Menu is already exist")
                return
            for menu in menu_list:
                menu_obj = SYSMenu.objects.create(**menu)
                print(menu_obj)
        except:
            print('Init fail')
            raise CommandError(traceback.print_exc())



