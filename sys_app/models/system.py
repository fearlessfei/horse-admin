# -*- coding: utf-8 -*-
# 为了灵活性与可迁移性，这里不使用django自带权限管理系统

from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from utils.date_time import now_timestamp10


class UserManager(BaseUserManager):
    """
    用户管理者
    """
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        """
        创建普通用户
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        创建超级用户
        :param username:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('status', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('status') is not True:
            raise ValueError('Superuser must have status=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class AbstractUser(AbstractBaseUser):
    """
    抽象用户类
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        abstract = True


class SYSUser(AbstractUser):
    """
    系统用户
    """
    id = models.AutoField(primary_key=True, verbose_name='用户ID')
    username = models.CharField(max_length=30, unique=True, default='', verbose_name='用户名')
    password = models.CharField(max_length=128, default='', verbose_name='用户密码')
    is_superuser = models.BooleanField(default=False, verbose_name='是否为超级管理员')
    email = models.CharField(max_length=100, default='', verbose_name='邮箱')
    phone = models.CharField(max_length=11, default='', verbose_name='手机号')
    reg_time = models.IntegerField(default=now_timestamp10, verbose_name='注册时间')
    last_login = models.IntegerField(default=now_timestamp10, verbose_name='最后登录时间')
    login_ip = models.CharField(max_length=30, default='', verbose_name='登录IP')
    avatar = models.CharField(max_length=100, default='', verbose_name='头像')
    order = models.IntegerField(default=10000, verbose_name='排序')
    creator = models.ForeignKey(to='self', null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'sys_user'
        ordering = ['order']


class SYSGroup(models.Model):
    """
    系统分组
    """
    id = models.AutoField(primary_key=True, verbose_name='组ID')
    name = models.CharField(max_length=30, unique=True, default='', verbose_name='组名')
    desc = models.CharField(max_length=100, default='', verbose_name='组描述')
    creator = models.ForeignKey(SYSUser, null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    created_time = models.IntegerField(default=now_timestamp10, verbose_name='创建时间')
    order = models.IntegerField(default=10000, verbose_name='组排序')

    class Meta:
        db_table = 'sys_group'
        ordering = ['order']


class SYSGroupUser(models.Model):
    """
    系统组用户
    """
    id = models.AutoField(primary_key=True, verbose_name='主键')
    group = models.ForeignKey(SYSGroup, verbose_name='分组', related_name='group_user', on_delete=models.CASCADE)
    user = models.ForeignKey(SYSUser, verbose_name='用户', related_name='user_group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sys_group_user'
        unique_together = ('group', 'user')


class SYSRole(models.Model):
    """
    系统角色
    """
    id = models.AutoField(primary_key=True, verbose_name='角色ID')
    name = models.CharField(max_length=50, unique=True, default='', verbose_name='角色名')
    desc = models.CharField(max_length=100, default='', verbose_name='角色描述')
    order = models.IntegerField(default=10000, verbose_name='角色排序')
    creator = models.ForeignKey(SYSUser, null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    create_time = models.IntegerField(default=now_timestamp10, verbose_name='创建时间')

    class Meta:
        db_table = 'sys_role'
        ordering = ['order']


class SYSUserRole(models.Model):
    """
    系统用户角色
    """
    id = models.AutoField(primary_key=True, verbose_name='主键')
    user = models.ForeignKey(SYSUser, verbose_name='用户', related_name='user_role', on_delete=models.CASCADE)
    role = models.ForeignKey(SYSRole, verbose_name='角色', related_name='role_user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sys_user_role'
        unique_together = ('user', 'role')


class SYSMenu(models.Model):
    """
    系统菜单
    """
    # 配置详情参考：https://panjiachen.github.io/vue-element-admin-site/zh/guide/essentials/router-and-nav.html#配置项
    id = models.AutoField(primary_key=True, verbose_name='菜单ID')
    parent_id = models.IntegerField(default=0, verbose_name='菜单父ID')
    path = models.CharField(max_length=255, default='', verbose_name='路径')
    component = models.CharField(max_length=255, default='', verbose_name='插件')
    redirect = models.CharField(max_length=255, default='', verbose_name='重定向')
    name = models.CharField(max_length=50, unique=True, default='', verbose_name='菜单名称')
    title = models.CharField(max_length=50, db_index=True, default='', verbose_name='标题')
    icon = models.CharField(max_length=30, default='', verbose_name='菜单图标')
    type = models.SmallIntegerField(default=0, verbose_name='菜单类型')
    perm_code = models.CharField(max_length=255, default='', verbose_name='权限代码')
    always_show = models.BooleanField(default=False, verbose_name='显示根路由')
    hidden = models.BooleanField(default=False, verbose_name='隐藏菜单')
    no_cache = models.BooleanField(default=False, verbose_name='不缓存')
    breadcrumb = models.BooleanField(default=True, verbose_name='面包屑')
    order = models.IntegerField(default=10000, verbose_name='菜单排序')
    status = models.BooleanField(default=True, verbose_name='菜单状态')
    creator = models.ForeignKey(SYSUser, null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    create_time = models.IntegerField(default=now_timestamp10, verbose_name='创建时间')

    class Meta:
        db_table = 'sys_menu'
        ordering = ['order']


class SYSRoleMenu(models.Model):
    """
    系统角色菜单操作
    """
    id = models.AutoField(primary_key=True, verbose_name='主键')
    role = models.ForeignKey(SYSRole, verbose_name='角色', related_name='role_menu', on_delete=models.CASCADE)
    menu = models.ForeignKey(SYSMenu, verbose_name='菜单', related_name='menu_role', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sys_role_menu'
        unique_together = ('role', 'menu')


class SYSGroupRole(models.Model):
    """
    系统组角色
    """
    related_name = 'user_role',
    id = models.AutoField(primary_key=True, verbose_name='主键')
    group = models.ForeignKey(SYSGroup, verbose_name='用户组', related_name='group_role', on_delete=models.CASCADE)
    role = models.ForeignKey(SYSRole, verbose_name='角色', related_name='role_group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sys_group_role'
        unique_together = ('group', 'role')
