# *-* coding: utf-8 *-*
import time

from django.contrib.auth import authenticate

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from utils import exceptions
from utils.perm import HasPerm

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    permission_code_list = HasPerm().get_user_perm_code_list(user.id)
    permission_codes = ','.join(permission_code_list)
    data = {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'avatar': user.avatar,
        'is_superuser': 1 if user.is_superuser else 0,
        'permission_codes': permission_codes
    }
    raise exceptions.Success(data=data, message='登录成功')


def validate(self, attrs):
    """
    登录验证
    :param self:
    :param attrs:
    :return:
    """
    request = self.context['request']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        client_ip = request.META['REMOTE_ADDR']

    credentials = {
        self.username_field: attrs.get(self.username_field),
        'password': attrs.get('password')
    }
    if all(credentials.values()):
        user = authenticate(**credentials)
        if user:
            if not user.status:
                raise exceptions.UserAccountDisabled()

            # 更新一下用户登录信息
            user.login_ip = client_ip
            user.last_login = int(time.time())
            user.save()

            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        else:
            raise exceptions.UserAccountError()
    else:
        raise exceptions.UserAccountValidationError()
JSONWebTokenSerializer.validate = validate