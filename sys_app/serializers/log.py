from .base import ContainCreatorModelSerializer

from sys_app.models import SYSLog


class LogSerializer(ContainCreatorModelSerializer):
    class Meta:
        model = SYSLog
        fields = '__all__'
