# *-* coding: utf-8 *-*
from rest_framework.validators import UniqueValidator

from .base import ContainCreatorModelSerializer
from sys_app.models import SYSRole


class RoleSerializer(ContainCreatorModelSerializer):
    """
    角色序列化
    """
    class Meta:
        model = SYSRole
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': [
                UniqueValidator(
                    queryset=SYSRole.objects.all(),
                    message='角色已存在'
                )
            ]}
        }

    def create(self, validated_data):
        role_instance = SYSRole.objects.create(**validated_data)
        return role_instance

    def update(self, instance, validated_data):
        for attr in validated_data:
            value = validated_data[attr]
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        return attrs