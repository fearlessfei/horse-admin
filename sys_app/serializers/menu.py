# *-* coding: utf-8 *-*
from enum import IntEnum

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .base import ContainCreatorModelSerializer
from sys_app.models import SYSMenu


class MenuType(IntEnum):
    ROOT = 0   # 目录
    MENU = 1   # 菜单
    BUTTON = 2 # 按钮


class MenuSerializer(ContainCreatorModelSerializer):
    """
    菜单序列化
    """
    def __init__(self, *args, **kwargs):
        self.menu_cond = kwargs.pop('menu_cond', {})
        super(self.__class__, self).__init__(*args, **kwargs)

    alwaysShow = serializers.CharField(source='always_show', read_only=True)
    meta = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = SYSMenu
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': [
                UniqueValidator(
                    queryset=SYSMenu.objects.all(),
                    message='菜单已存在'
                )
            ]},
            'path': {'required': True, 'allow_blank': True},
            'perm_code': {'required': True, 'allow_blank': True},
            'component': {'required': True, 'allow_blank': True},
            'redirect': {'required': True, 'allow_blank': True},
            'create_time': {'read_only': True},
        }

    def get_meta(self, obj):
        meta = {
            'title': obj.title,
            'icon': obj.icon,
            'no_cache': obj.no_cache,
            'breadcrumb': obj.breadcrumb,
        }
        return meta

    def get_children(self, obj):
        tree = {}
        data_list = list(SYSMenu.objects.filter(**self.menu_cond).values())
        for data in data_list:
            data['alwaysShow'] = data['always_show']
            data['meta'] = {
                'title': data['title'],
                'icon': data['icon'],
                'no_cache': data['no_cache'],
                'breadcrumb': data['breadcrumb'],
            }
            tree[data["id"]] = data
        self.add_child_menu(data_list, obj.id, tree)
        if obj.id in tree:
            return tree[obj.id].get('children', [])
        return []

    def add_child_menu(cls, data_list, menu_id, tree):
        for data in data_list:
            parent_id = data['parent_id']
            if menu_id == parent_id:
                if "children" not in tree[parent_id]:
                    tree[parent_id]["children"] = []
                tree[parent_id]["children"].append(data)
                cls.add_child_menu(data_list, data['id'], tree)

    def create(self, validated_data):
        role_instance = SYSMenu.objects.create(**validated_data)
        return role_instance

    def update(self, instance, validated_data):
        for attr in validated_data:
            value = validated_data[attr]
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        parent_id = attrs['parent_id']
        menu_type = attrs['type']
        if menu_type in (MenuType.MENU, MenuType.BUTTON) and not parent_id:
            raise serializers.ValidationError('必须选择一个父节点')

        return attrs