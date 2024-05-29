from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CommonPagimation(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommonViewSet(viewsets.ModelViewSet):
    pagination_class = CommonPagimation

    def perform_create(self, serializer):
        if serializer.is_valid():
            if "created_by" in serializer.get_fields().keys():
                serializer.save(created_by=self.request.user)
            return super().perform_create(serializer)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if not hasattr(self, 'advance_search'):
            return queryset
        for search_param in self.advance_search:
            query_param = search_param['query_param']
            filter_query = search_param['filter_query']
            value_types = search_param['value_types']

            param_value = self.request.query_params.get(query_param)
            if param_value is not None and param_value != 'undefined' and param_value:
                if bool in value_types:
                    param_value = param_value.lower() == 'true'
                if list in value_types:
                    try:
                        param_value = param_value.split(',')
                    except ValueError:
                        raise ValidationError(f"Validation error on value of filter {query_param}")
                # Check if the parameter value is of the expected type
                if any(isinstance(param_value, value_type) for value_type in value_types):
                    # Filter the queryset based on the parameter
                    filter_args = {f'{filter_query}': param_value}
                    queryset = queryset.filter(**filter_args)

        return queryset
