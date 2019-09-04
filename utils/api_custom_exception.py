# *-* coding: utf-8 *-*
from rest_framework.response import Response
from rest_framework import exceptions, status

from .exceptions import (
    ExceptionBase,
    ParseError,
    AuthenticationFailed,
    NotAuthenticated,
)


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc:　异常实例
    :param context:　抛出异常的上下文
    :return:
    """
    headers = {}

    # 内部抛出的异常
    if isinstance(exc, exceptions.APIException):
        exception = exc

        exception.status_code = status.HTTP_200_OK
        exception.code = ParseError().code
        exception.message = exc.detail

        # jwt 内部抛出的异常在这里重写
        if isinstance(exc, exceptions.AuthenticationFailed):
            exception.code = AuthenticationFailed().code
            exception.message = AuthenticationFailed().message
        elif isinstance(exc, exceptions.NotAuthenticated):
            exception.code = NotAuthenticated().code
            exception.message = NotAuthenticated().message
        else:
            exception.status_code = exc.status_code
    #　自定义抛出的异常
    elif isinstance(exc, ExceptionBase):
        exception = exc
    else:
        return None

    data = dict(
        code=exception.code,
        message=exception.message,
    )
    if hasattr(exception, 'data'):
        data['data'] = exception.data

    return Response(data, status=exception.status_code, headers=headers)
