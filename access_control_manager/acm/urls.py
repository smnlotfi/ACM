from django.urls import include, path
from rest_framework import routers

from .views import GroupPermissionsViewSet, UserGroupViewSet

router = routers.DefaultRouter()
router.register(r'group-permissions', GroupPermissionsViewSet)
router.register(r'user-group', UserGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
