# *-* coding: utf-8 *-*
from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.routers import DefaultRouter

from sys_app.views.user import userViewSet
from sys_app.views.role import RoleViewSet
from sys_app.views.role_menu import RoleMenuViewSet
from sys_app.views.menu import MenuViewSet
from sys_app.views.user_menu import UserMenuViewSet
from sys_app.views.group import GroupViewSet
from sys_app.views.group_user import GroupUserViewSet

urlpatterns = [
    url(r'^user/login$', obtain_jwt_token),
    url(r'^user/refresh/token$', refresh_jwt_token),
]

router = DefaultRouter(trailing_slash=False)
router.register(r'user/menu', UserMenuViewSet)
router.register(r'user', userViewSet)
router.register(r'role/menu', RoleMenuViewSet)
router.register(r'role', RoleViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'group/user', GroupUserViewSet)
router.register(r'group', GroupViewSet)

urlpatterns += router.urls
