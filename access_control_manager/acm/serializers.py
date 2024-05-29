from rest_framework import serializers

from .models import GroupPermissions, UserGroup


class EndpointPermissionSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    method = serializers.ChoiceField(choices=(
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),),
        required=True
    )


class ModelPermissionSerializer(serializers.Serializer):
    model_name = serializers.CharField(required=True)
    access = serializers.ListSerializer(child=serializers.ChoiceField(choices=(
        ("READ", "READ"),
        ("CREATE", "CREATE"),
        ("UPDATE", "UPDATE"),
        ("DELETE", "DELETE"),)
    ), required=True)


class GroupPermissionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermissions
        fields = [
            'id',
            'name',
            'permission_type',
            'permission_key',
            'extra_fields',
            'created_at',
            'created_by'
        ]

    EXTRA_FIELD_SERIALIZER_MAPPER = {
        "endpoint": EndpointPermissionSerializer,
        "model": ModelPermissionSerializer,

    }

    def validate(self, data):
        data = super(GroupPermissionsModelSerializer, self).validate(data)
        permission_type = data.get('permission_type', None)
        extra_fields = data.get('extra_fields', {})
        serializer_class = self.EXTRA_FIELD_SERIALIZER_MAPPER.get(permission_type)
        if not serializer_class:
            raise serializers.ValidationError(f"permission_type {permission_type} not supported.")
        serializer_class = serializer_class(many=False, data=extra_fields)
        if serializer_class.is_valid():
            return data
        else:
            raise serializers.ValidationError({"extra_fields": serializer_class.errors})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        permission_type = data.get('permission_type', None)
        extra_fields = data.get('extra_fields', {})
        serializer_class = self.EXTRA_FIELD_SERIALIZER_MAPPER.get(permission_type)
        if not serializer_class:
            raise serializers.ValidationError(f"permission_type {permission_type} not supported.")
        serializer_class = serializer_class(extra_fields, many=False)
        data["extra_fields"] = serializer_class.data
        return data


class UserGroupModelSerializer(serializers.ModelSerializer):
    # permissions = GroupPermissionsModelSerializer(write_only=True, many=True)

    class Meta:
        model = UserGroup
        fields = [
            'id',
            'name',
            'description',
            'members',
            'permissions',
            'created_at',
            'created_by'
        ]
