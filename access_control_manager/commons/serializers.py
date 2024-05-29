from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Model


class NestedModeSerializerMixin(serializers.ModelSerializer):
    def get_nested_serializers(self, *args, **kwargs):
        if not getattr(self.Meta, 'nested_serializers', None):
            raise ImproperlyConfigured(
                "nested_serializers is required in Meta class to use the NestedModeSerializerMixin")
        nested_serializers = self.Meta.nested_serializers
        if not isinstance(nested_serializers, dict):
            raise ImproperlyConfigured("nested_serializers must be a instance of dict.")
        for child_serializer in nested_serializers.values():
            if not isinstance(child_serializer, dict):
                raise ImproperlyConfigured("nested_serializers values must be a instance of dict.")
            if "model" not in child_serializer or "many" not in child_serializer:
                raise ImproperlyConfigured("nested_serializers values must contain 'model' and 'many' fields")
        return nested_serializers

    def to_internal_value(self, data):
        nested_serializers = self.get_nested_serializers()
        internal_data = super().to_internal_value(data)
        for child_serializer_key in nested_serializers:
            is_many = nested_serializers[child_serializer_key].get("many")
            child_pk = data.get(child_serializer_key, None)
            # Skip if nested data is not provided
            if child_pk is None:
                continue
            if is_many:
                child_pk = data.get(child_serializer_key, None)
            else:
                child_pk = [data.get(child_serializer_key, None)]
            child_list = []
            for item in child_pk:
                if not isinstance(item, int) and not isinstance(item, str):
                    raise ValidationError(
                        {child_serializer_key: [
                            f'Invalid {child_serializer_key} primary key, expected integer, string got {type(item).__name__} instead']},
                        code='invalid',
                    )
                try:
                    child_model = nested_serializers[child_serializer_key].get("model")
                    child_item = child_model.objects.get(pk=item)
                    child_list.append(child_item)
                except child_model.DoesNotExist:
                    raise ValidationError(
                        {child_serializer_key: [f'Invalid {child_serializer_key} primary key, Not found.']},
                        code='invalid',
                    )
            if is_many:
                internal_data[child_serializer_key] = child_list
            else:
                internal_data[child_serializer_key] = child_list[0] if child_list else None
        return internal_data
