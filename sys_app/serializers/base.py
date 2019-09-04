# *-* coding: utf-8 *-*
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """
    序列化基类
    """
    class Meta:
        pass


class BaseModelSerializer(serializers.ModelSerializer):
    """
    模型序列化基类
    """
    class Meta:
        pass


class ContainCreatorModelSerializer(BaseModelSerializer):
    """
    包含创建人模型序列化
    """
    creator = serializers.SerializerMethodField()

    def get_creator(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return 'deleted'