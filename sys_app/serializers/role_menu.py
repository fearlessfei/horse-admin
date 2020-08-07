# *-* coding: utf-8 *-*
import traceback

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .base import BaseModelSerializer
from .menu import MenuSerializer
from sys_app.models import (
    SYSRole,
    SYSMenu,
    SYSRoleMenu
)


class RoleMenuSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, menu_id):
        try:
            return self.get_queryset().get(**{'id': menu_id})
        except ObjectDoesNotExist:
            raise serializers.ValidationError('无效的菜单')
        except (TypeError, ValueError):
            raise serializers.ValidationError('无效的菜单类型')


class RoleMenuSerializer(BaseModelSerializer):
    """
    角色菜单序列化
    """
    menu = serializers.SerializerMethodField()
    role_menu = RoleMenuSlugRelatedField(
        many=True,
        queryset=SYSMenu.objects.all(),
        slug_field='menu_id',
        allow_null=True,
    )

    class Meta:
        model = SYSRole
        fields = '__all__'

    def get_menu(self, instance):
        queryset = SYSMenu.objects.filter(parent_id=0)

        is_superuser = self.context['view'].request.user.is_superuser
        if not is_superuser:
            objs = SYSRoleMenu.objects.filter(role=instance)
            queryset = queryset.filter(id__in=[obj.menu.id for obj in objs])

        return MenuSerializer(instance=queryset, many=True).data

    def update(self, instance, validated_data):
        role_menu = validated_data.pop('role_menu', [])

        try:
            with transaction.atomic():
                SYSRoleMenu.objects.filter(role=instance).delete()
                role_menu_list = [
                    SYSRoleMenu(role=instance, menu=menu)
                    for menu in role_menu
                ]
                SYSRoleMenu.objects.bulk_create(role_menu_list)
        except:
            traceback.print_exc()
            raise serializers.ValidationError('角色权限更新失败')

        return instance
