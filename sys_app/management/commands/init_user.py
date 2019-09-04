# *-* coding: utf-8 *-*
import time
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

user = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # 初始化一个超级管理员
            init_data = dict(
                username='admin',
                password='123456',
                is_superuser=1,
                status=1,
                creator_id=1,
                avatar='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                reg_time=int(time.time()),
                last_login=int(time.time()),
            )
            if user.objects.filter(username='admin'):
                print("User is already exist")
                return
            user_obj = user.objects.create_user(**init_data)
            print(user_obj)
            print('Init success')
        except:
            print('Init fail')
            raise CommandError(traceback.print_exc())

