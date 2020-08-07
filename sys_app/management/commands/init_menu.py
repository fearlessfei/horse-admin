# *-* coding: utf-8 *-*
from collections import OrderedDict
from sys_app.models import SYSMenu
from django.core.management.base import BaseCommand

custom_menus = {
    'sys': {
        "path": "/sys",
        "component": "index",
        "redirect": "/",
        "title": "系统管理",
        "icon": "sys",
        "type": 0,
        "perm_code": "",
        "creator_id": 1,
        "children": {
            "sys_user": {
                "path": "user",
                "component": "sys/user/index",
                "redirect": "",
                "title": "用户管理",
                "icon": "user",
                "type": 1,
                "perm_code": "",
                "creator_id": 1,
                "children": {
                    "sys_user_create": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "创建",
                        "icon": "create",
                        "type": 2,
                        "perm_code": "sys:user:create",
                        "creator_id": 1
                    },
                    "sys_user_select": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "查询",
                        "icon": "select",
                        "type": 2,
                        "perm_code": "sys:user:select",
                        "creator_id": 1
                    },
                    "sys_user_edit": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "编辑",
                        "icon": "edit",
                        "type": 2,
                        "perm_code": "sys:user:edit",
                        "creator_id": 1
                    },
                    "sys_user_delete": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "删除",
                        "icon": "delete",
                        "type": 2,
                        "perm_code": "sys:user:delete",
                        "creator_id": 1
                    },
                },
            },
            "sys_role": {
                "path": "role",
                "component": "sys/role/index",
                "redirect": "",
                "title": "角色管理",
                "icon": "role",
                "type": 1,
                "perm_code": "",
                "creator_id": 1,
                "children": {
                    "sys_role_edit": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "编辑",
                        "icon": "edit",
                        "type": 2,
                        "perm_code": "sys:role:edit",
                        "creator_id": 1
                    },
                    "sys_role_delete": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "删除",
                        "icon": "delete",
                        "type": 2,
                        "perm_code": "sys:role:delete",
                        "creator_id": 1
                    },
                    "sys_role_select": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "查询",
                        "icon": "select",
                        "type": 2,
                        "perm_code": "sys:role:select",
                        "creator_id": 1
                    },
                    "sys_role_create": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "创建",
                        "icon": "create",
                        "type": 2,
                        "perm_code": "sys:role:create",
                        "creator_id": 1
                    },
                    "sys_role_perm": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "权限",
                        "icon": "perm",
                        "type": 2,
                        "perm_code": "sys:role:perm",
                        "creator_id": 1
                    },
                },
            },
            "sys_menu": {
                "path": "menu",
                "component": "sys/menu/index",
                "redirect": "",
                "title": "菜单管理",
                "icon": "nested",
                "type": 1,
                "perm_code": "",
                "creator_id": 1,
                "children": {
                    "sys_menu_select": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "查询",
                        "icon": "select",
                        "type": 2,
                        "perm_code": "sys:menu:select",
                        "creator_id": 1
                    },
                    "sys_menu_create": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "创建",
                        "icon": "create",
                        "type": 2,
                        "perm_code": "sys:menu:create",
                        "creator_id": 1
                    },
                    "sys_menu_edit": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "编辑",
                        "icon": "edit",
                        "type": 2,
                        "perm_code": "sys:menu:edit",
                        "creator_id": 1
                    },
                    "sys_menu_delete": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "删除",
                        "icon": "delete",
                        "type": 2,
                        "perm_code": "sys:menu:delete",
                        "creator_id": 1
                    },
                }
            },
            "sys_group": {
                "path": "group",
                "component": "sys/group/index",
                "redirect": "",
                "title": "用户组管理",
                "icon": "group",
                "type": 1,
                "perm_code": "",
                "creator_id": 1,
                "children": {
                    "sys_group_select": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "查询",
                        "icon": "select",
                        "type": 2,
                        "perm_code": "sys:group:select",
                        "creator_id": 1
                    },
                    "sys_group_create": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "创建",
                        "icon": "create",
                        "type": 2,
                        "perm_code": "sys:group:create",
                        "creator_id": 1
                    },
                    "sys_group_edit": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "编辑",
                        "icon": "edit",
                        "type": 2,
                        "perm_code": "sys:group:edit",
                        "creator_id": 1
                    },
                    "sys_group_delete": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "删除",
                        "icon": "delete",
                        "type": 2,
                        "perm_code": "sys:group:delete",
                        "creator_id": 1
                    },
                    "sys_group_user": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "用户",
                        "icon": "perm",
                        "type": 2,
                        "perm_code": "sys:group:user",
                        "creator_id": 1
                    },
                }
            },
            "sys_log": {
                "path": "log",
                "component": "sys/log/index",
                "redirect": "",
                "title": "系统日志",
                "icon": "log",
                "type": 1,
                "perm_code": "",
                "creator_id": 1,
                "children": {
                    "sys_log_select": {
                        "path": "",
                        "component": "",
                        "redirect": "",
                        "title": "查询",
                        "icon": "select",
                        "type": 2,
                        "perm_code": "sys:log:select",
                        "creator_id": 1
                    },
                }
            },
        },
    }
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ 以json格式配置菜单"""
        menu_dict = OrderedDict()
        self.__get_all_names(custom_menus, menu_dict)
        SYSMenu.objects.exclude(name__in=list(menu_dict.keys())).delete()

        name_id_mapping = {}

        for name, menu in menu_dict.items():
            parent_id = 0
            parent_name = menu.pop('__parent_name', None)
            if parent_name is not None:
                parent_id = name_id_mapping.get(parent_name) or SYSMenu.objects.filter(name=parent_name).first().id
            menu['parent_id'] = parent_id
            obj, created = SYSMenu.objects.update_or_create(name=name, defaults=menu)
            name_id_mapping[name] = obj.id

    def __get_all_names(self, menus, menu_dict, parent_name=None):
        for name, menu in menus.items():
            children = menu.pop('children', None)
            menu['__parent_name'] = parent_name
            menu_dict[name] = menu
            if children and len(children):
                self.__get_all_names(children, menu_dict, name)


if __name__ == '__main__':
    Command().handle()
