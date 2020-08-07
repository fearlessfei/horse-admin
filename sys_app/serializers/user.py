# *-* coding: utf-8 *-*
import traceback

from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import ContainCreatorModelSerializer
from sys_app.models import SYSUserRole, SYSRole

User = get_user_model()


class UserRoleSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, role_id):
        try:
            return self.get_queryset().get(**{'id': role_id})
        except ObjectDoesNotExist:
            raise serializers.ValidationError('无效的角色')
        except (TypeError, ValueError):
            raise serializers.ValidationError('无效的角色类型')


class UserSerializer(ContainCreatorModelSerializer):
    """
    用户序列化
    """
    user_role = UserRoleSlugRelatedField(
        many=True,
        queryset=SYSRole.objects.all(),
        slug_field='role_id',
        allow_null=True,
    )

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'avatar': {'required': True, 'allow_blank': True},
            'password': {'required': True, 'allow_blank': True},
            'login_ip': {'read_only': True},
            'reg_time': {'read_only': True},
            'last_login': {'read_only': True},
            'username': {'validators': [
                UniqueValidator(
                    queryset=User.objects.all(),
                    message='用户已存在'
                )
            ]}
        }

    def create(self, validated_data):
        user_role = validated_data.pop('user_role', [])

        try:
            with transaction.atomic():
                validated_data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
                user_instance = User.objects.create_user(**validated_data)
                # 批量创建用户角色
                create_data_list = [
                    SYSUserRole(user=user_instance, role=role)
                    for role in user_role
                ]
                SYSUserRole.objects.bulk_create(create_data_list)

                return user_instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError('用户创建失败')

    def update(self, instance, validated_data):
        user_role = validated_data.pop('user_role', [])

        try:
            with transaction.atomic():
                SYSUserRole.objects.filter(user=instance).delete()
                user_role_list = [
                    SYSUserRole(user=instance,role=role)
                    for role in user_role
                ]
                SYSUserRole.objects.bulk_create(user_role_list)

                for attr in validated_data:
                    value = validated_data[attr]
                    if attr == 'password':
                        if value:
                            instance.set_password(value)
                        continue
                    setattr(instance, attr, value)
                instance.save()
        except:
            traceback.print_exc()
            raise serializers.ValidationError('用户信息更新失败')

        return instance

    def validate(self, attrs):
        return attrs
