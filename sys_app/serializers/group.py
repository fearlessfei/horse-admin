# *-* coding: utf-8 *-*
import traceback

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import ContainCreatorModelSerializer
from sys_app.models import (
    SYSGroup,
    SYSGroupRole,
    SYSRole
)

User = get_user_model()


class GroupRoleSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, role_id):
        try:
            return self.get_queryset().get(**{'id': role_id})
        except ObjectDoesNotExist:
            raise serializers.ValidationError('无效的角色')
        except (TypeError, ValueError):
            raise serializers.ValidationError('无效的角色类型')


class GroupUserSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, user_id):
        try:
            return self.get_queryset().get(**{'id': user_id})
        except ObjectDoesNotExist:
            raise serializers.ValidationError('无效的用户')
        except (TypeError, ValueError):
            raise serializers.ValidationError('无效的用户类型')


class GroupSerializer(ContainCreatorModelSerializer):
    """
    组序列化
    """
    group_role = GroupRoleSlugRelatedField(
        many=True,
        queryset=SYSRole.objects.all(),
        slug_field='role_id',
        allow_null=True,
    )

    class Meta:
        model = SYSGroup
        fields = '__all__'
        extra_kwargs = {
            'desc': {'required': True},
            'name': {'validators': [
                UniqueValidator(
                    queryset=SYSGroup.objects.all(),
                    message='组已存在'
                )
            ]}
        }

    def create(self, validated_data):
        group_role = validated_data.pop('group_role', [])

        try:
            with transaction.atomic():
                group_instance = SYSGroup.objects.create(**validated_data)
                # 批量创建组角色
                create_data_list = [
                    SYSGroupRole(group=group_instance, role=role)
                    for role in group_role
                ]
                SYSGroupRole.objects.bulk_create(create_data_list)

                return group_instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError('组创建失败')

    def update(self, instance, validated_data):
        group_role = validated_data.pop('group_role', [])

        try:
            with transaction.atomic():
                SYSGroupRole.objects.filter(group=instance).delete()
                group_role_objs = [
                    SYSGroupRole(group=instance, role=role)
                    for role in group_role
                ]
                SYSGroupRole.objects.bulk_create(group_role_objs)

                for attr in validated_data:
                    value = validated_data[attr]
                    setattr(instance, attr, value)
                instance.save()
        except:
            traceback.print_exc()
            raise serializers.ValidationError('组信息更新失败')

        return instance

    def validate(self, attrs):
        return attrs
