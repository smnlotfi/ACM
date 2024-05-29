from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .services.acm_services import ACMService
from django.core.exceptions import PermissionDenied


class AbstractModelQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        if getattr(self.model, "exposed_request", None):

            has_permission = ACMService.has_user_model_permission(request=self.model.exposed_request,
                                                                  model_name=self.model.__name__,
                                                                  access="READ")

            if not has_permission:
                raise PermissionDenied()
        # Always include a default condition
        kwargs.setdefault('is_soft_deleted', False)
        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        if getattr(self.model, "exposed_request", None):

            has_permission = ACMService.has_user_model_permission(request=self.model.exposed_request,
                                                                  model_name=self.model.__name__,
                                                                  access="READ")
            if not has_permission:
                raise PermissionDenied()
        return super().get(*args, **kwargs)


class AbstractModel(models.Model):
    is_soft_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   help_text=_('Automatically set who was created this record.'),
                                   related_name="%(app_label)s_%(class)s_related")
    objects = AbstractModelQuerySet.as_manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if getattr(self, "exposed_request", None):
            has_permission = ACMService.has_user_model_permission(request=self.exposed_request,
                                                                  model_name=self.__class__.__name__,
                                                                  access="DELETE")
            if not has_permission:
                raise PermissionDenied()
        self.is_soft_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:
            access = "UPDATE"
        else:
            access = "CREATE"
        if getattr(self, "exposed_request", None):
            has_permission = ACMService.has_user_model_permission(request=self.exposed_request,
                                                                  model_name=self.__class__.__name__,
                                                                  access=access)
            if not has_permission:
                raise PermissionDenied()
        super().save(*args, **kwargs)


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, is_archive=True or False)
        obj.is_soft_deleted = False
        obj.save()
        return obj

    @classmethod
    def new_or_update(cls, data):
        try:
            obj = cls.load()
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        except Exception as e:
            raise e[0]

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)


class MainViewset(ModelViewSet):
    pass


class MainAPIView(APIView):
    pass
