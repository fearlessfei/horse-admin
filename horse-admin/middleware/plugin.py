# *-* coding: utf-8 *-*
import traceback

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.exceptions import Fail

fail =Fail()


class BasedExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        traceback.print_exc()
        return JsonResponse(dict(code=fail.code, message="服务内部异常"))
