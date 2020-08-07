# *-* coding: utf-8 *-*
from rest_framework import status


class ExceptionBase(Exception):
    """
    异常基类
    """
    def __init__(self, code=0, message="", data=None, status_code=status.HTTP_200_OK):
        if data is not None:
            self.data = data

        self.status_code = status_code
        self.code = code
        self.message = message

    def __str__(self):
        print("<status_code: {0}, code: {1}, message: {2}, data: {3}".format(
            self.status_code,
            self.code,
            self.message,
            self.data)
        )


class Success(ExceptionBase):
    """
    返回成功
    """
    def __init__(self, code=20000, message="成功", data=None):
        super(self.__class__, self).__init__(code, message, data)


class Fail(ExceptionBase):
    """
    返回失败
    """
    def __init__(self, code=50000, message="失败", data=None):
        super(self.__class__, self).__init__(code, message, data)


class ParseError(ExceptionBase):
    def __init__(self, code=40000, message="无效的请求", data=None):
        super(self.__class__, self).__init__(code, message, data)


class AuthenticationFailed(ExceptionBase):
    def __init__(self, code=40001, message="登录失效，请重新登录", data=None):
        super(self.__class__, self).__init__(code, message, data)


class NotAuthenticated(ExceptionBase):
    def __init__(self, code=40002, message="认证失败", data=None):
        super(self.__class__, self).__init__(code, message, data)


class UserAccountDisabled(ExceptionBase):
    """
    用户账号被禁用
    """
    def __init__(self, code=40003, message="您的账号被禁用，请联系管理员", data=None):
        super(self.__class__, self).__init__(code, message, data)


class UserAccountError(ExceptionBase):
    """
    用户账号错误
    """
    def __init__(self, code=40004, message="用户名或密码有误", data=None):
        super(self.__class__, self).__init__(code, message, data)


class UserAccountValidationError(ExceptionBase):
    """
    用户账号验证错误
    """
    def __init__(self, code=40005, message="用户名或密码不能为空", data=None):
        super(self.__class__, self).__init__(code, message, data)


class PermissionDenied(ExceptionBase):
    """
    权限被拒绝
    """
    def __init__(self, code=40006, message="没有权限操作", data=None):
        super(self.__class__, self).__init__(code, message, data)
