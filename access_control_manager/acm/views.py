from commons.views import CommonViewSet
from drf_spectacular.types import OpenApiTypes
from rest_framework import permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework_api_key.permissions import HasAPIKey

from .models import GroupPermissions, UserGroup
from .serializers import GroupPermissionsModelSerializer, UserGroupModelSerializer
from .exceptions import URLPermissionDoesntExist, ModelPermissionDoesntExist

User = get_user_model()


class GroupPermissionsViewSet(CommonViewSet):
    """
        Model view set for have CRUD on GroupPermissions model.
    """
    queryset = GroupPermissions.objects.all()
    serializer_class = GroupPermissionsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'permission_key', 'extra_fields']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', 'name', 'permission_type', 'created_by', 'created_at')
    ordering = ('-created_at')


class UserGroupViewSet(CommonViewSet):
    """
        Model view set for have CRUD on UserGroup model.
    """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('id', 'name', 'created_by', 'created_at')
    ordering = ('-created_at')

    @extend_schema(parameters=[
        OpenApiParameter("user_id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True),
        OpenApiParameter("model_name", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
    ])
    @action(detail=False, methods=['get'], url_path=r'get_model_permissions',
            permission_classes=[permissions.IsAuthenticated | HasAPIKey])
    def get_model_permission(self, request, *args, **kwargs):
        """
        Get all permission for specified model name that assigned to user.

        return 200 with data field

        return 404 if there was no permission for that model.
        """
        model_name = request.query_params.get('model_name', None)
        user_id = request.query_params.get('user_id', None)
        user = User.objects.filter(id=user_id).first()
        if not model_name or not user_id or not user:
            return Response({"message": "Invalid model name or user id."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            model_permissions = UserGroup.get_user_model_permissions(user=user, model_name=model_name)
            return Response({"data": GroupPermissionsModelSerializer(model_permissions, many=True).data},
                            status=status.HTTP_200_OK)
        except ModelPermissionDoesntExist:
            return Response({"message": "there is no permission for this model name."},
                            status=status.HTTP_404_NOT_FOUND)

    @extend_schema(parameters=[
        OpenApiParameter("user_id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True),
        OpenApiParameter("endpoint_url", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
        OpenApiParameter("method", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True)
    ])
    @action(detail=False, methods=['get'],
            url_path=r'get_endpoint_permissions',
            permission_classes=[permissions.IsAuthenticated | HasAPIKey])
    def get_endpoint_permission(self, request, *args, **kwargs):
        """
        Get all permission for specified endpoint that assigned to user.

        return 200 with data field

        return 404 if there was no permission for that endpoint.
        """
        user_id = request.query_params.get('user_id', None)
        endpoint_url = request.query_params.get('endpoint_url', None)
        method = request.query_params.get('method', None)
        user = User.objects.filter(id=user_id).first()
        if not endpoint_url or not method and not user_id or not user:
            return Response({"message": "Invalid endpoint url or user id."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            endpoint_permissions = UserGroup.get_user_endpoint_permissions(user=user, endpoint_url=endpoint_url,
                                                                           method=method)
            return Response({"data": GroupPermissionsModelSerializer(endpoint_permissions, many=True).data},
                            status=status.HTTP_200_OK)
        except URLPermissionDoesntExist:
            return Response({"message": "there is no permission for this endpoint."},
                            status=status.HTTP_404_NOT_FOUND)

    @extend_schema(parameters=[OpenApiParameter("user_id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=True)])
    @action(detail=False, methods=['get'], url_path=r'get_all_permissions',
            permission_classes=[permissions.IsAuthenticated | HasAPIKey])
    def get_all_permission(self, request, *args, **kwargs):
        """
        Get all permission that assigned to user.

        return 200 with data field
        """
        user_id = request.query_params.get('user_id', None)
        user = User.objects.filter(id=user_id).first()
        if not user_id or not user:
            return Response({"message": "Invalid user id."},
                            status=status.HTTP_400_BAD_REQUEST)
        all_user_permissions = UserGroup.get_user_permissions(user=user)
        return Response({"data": GroupPermissionsModelSerializer(many=True, instance=all_user_permissions).data},
                        status=status.HTTP_200_OK)
