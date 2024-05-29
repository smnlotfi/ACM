from commons.constants import DEFAULT_CHARFIELD_MAX_LEN
from commons.models import AbstractModel
from django.contrib.auth import get_user_model
from django.db import models

from .exceptions import URLPermissionDoesntExist,ModelPermissionDoesntExist

User = get_user_model()

PERMISSION_TYPE_CHOICES = (
    ('endpoint', 'endpoint'),
    ('model', 'model'),
    ('action', 'action'),
    ('page', 'page')
)
MODEL_PERMISSION_TYPE = 'model'
ENDPOINT_PERMISSION_TYPE = 'endpoint'


class GroupPermissions(AbstractModel):
    name = models.CharField(max_length=DEFAULT_CHARFIELD_MAX_LEN, unique=True)
    permission_type = models.CharField(max_length=24, choices=PERMISSION_TYPE_CHOICES)
    permission_key = models.CharField(max_length=DEFAULT_CHARFIELD_MAX_LEN, unique=True)
    extra_fields = models.JSONField(default=dict)


class UserGroup(AbstractModel):
    name = models.CharField(null=True, blank=True, max_length=DEFAULT_CHARFIELD_MAX_LEN)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True)
    permissions = models.ManyToManyField(GroupPermissions, null=True, blank=True)

    @staticmethod
    def get_user_permissions(user):
        user_permissions = []
        groups_user_member = UserGroup.objects.filter(members__in=[user])
        for group in groups_user_member:
            group_permissions = group.permissions.all()
            for permission in group_permissions:
                user_permissions.append(permission)
        return user_permissions

    @staticmethod
    def get_user_model_permissions(user, model_name):
        if not UserGroup.is_model_have_permission(model_name=model_name):
            raise ModelPermissionDoesntExist
        user_permissions = UserGroup.get_user_permissions(user)
        model_related_permissions = []
        for permission in user_permissions:
            if permission.permission_type == MODEL_PERMISSION_TYPE and permission.extra_fields.get("model_name",
                                                                                                   None) == model_name:
                model_related_permissions.append(permission)
        return model_related_permissions

    @staticmethod
    def is_url_have_permission(url):
        endpoint_permissions = GroupPermissions.objects.filter(permission_type=ENDPOINT_PERMISSION_TYPE,
                                                               extra_fields__url=url)
        return bool(endpoint_permissions)
    @staticmethod
    def is_model_have_permission(model_name):
        endpoint_permissions = GroupPermissions.objects.filter(permission_type=MODEL_PERMISSION_TYPE,
                                                               extra_fields__model_name=model_name)
        return bool(endpoint_permissions)

    @staticmethod
    def get_user_endpoint_permissions(user, endpoint_url, method):
        if not UserGroup.is_url_have_permission(endpoint_url):
            raise URLPermissionDoesntExist
        user_permissions = UserGroup.get_user_permissions(user)
        endpoint_related_permissions = []
        for permission in user_permissions:
            if (permission.permission_type == ENDPOINT_PERMISSION_TYPE and
                    permission.extra_fields.get("url", None) == endpoint_url and
                    permission.extra_fields.get("method", "").upper() == method.upper()):
                endpoint_related_permissions.append(permission)
        return endpoint_related_permissions
