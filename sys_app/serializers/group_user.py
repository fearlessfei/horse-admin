# *-* coding: utf-8 *-*
import traceback

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .base import BaseModelSerializer
from sys_app.models import (
    SYSGroup,
    SYSGroupUser
)

User = get_user_model()


class GroupUserSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, user_id):
        try:
            return self.get_queryset().get(**{'id': user_id})
        except ObjectDoesNotExist:
            raise serializers.ValidationError('无效的用户')
        except (TypeError, ValueError):
            raise serializers.ValidationError('无效的用户类型')


class GroupUserSerializer(BaseModelSerializer):
    """
    组用户序列化
    """
    user = serializers.SerializerMethodField()
    group_user = GroupUserSlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='user_id',
        allow_null=True,
    )

    class Meta:
        model = SYSGroup
        fields = '__all__'

    def get_user(self, obj):
        user_list = []

        queryset = User.objects.filter()
        for qs in queryset:
            user_list.append(dict(
                user_id=qs.id,
                username=qs.username,
            ))
        return user_list

    def update(self, instance, validated_data):
        group_user = validated_data.pop('group_user', [])

        try:
            with transaction.atomic():
                SYSGroupUser.objects.filter(group=instance).delete()
                group_user_list = [
                    SYSGroupUser(group=instance, user=user)
                    for user in group_user
                ]
                SYSGroupUser.objects.bulk_create(group_user_list)
        except:
            traceback.print_exc()
            raise serializers.ValidationError('组用户更新失败')

        return instance
