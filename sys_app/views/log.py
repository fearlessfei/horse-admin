from sys_app.models import (
    SYSLog,
    SYSUser
)
from sys_app.serializers.log import LogSerializer
from sys_app.views.base import AuthAPIViewSet
from utils.perm import HasPerm


class LogViewSet(AuthAPIViewSet):
    queryset = SYSLog.objects.all()
    serializer_class = LogSerializer

    @property
    def prune_query_params(self):
        """
        查询参数
        :return:
        """
        params = {}

        query_params = self.request.query_params
        for k in query_params:
            if k not in ['page', 'limit'] and query_params[k]:
                if k == 'creator':
                    params[k] = 0
                    userObj = SYSUser.objects.filter(username=query_params[k]).first()
                    if userObj:
                        params[k] = userObj.id
                elif k == 'start_time':
                    params['create_time__gte'] = query_params[k]
                elif k == 'end_time':
                    params['create_time__lte'] = query_params[k]

        return params

    @HasPerm(perm_code='sys:log:select')
    def list(self, request, *args, **kwargs):
        super(self.__class__, self).list(request, *args, **kwargs)
