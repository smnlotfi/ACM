# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

def custom_exception_handler(exc, context):
    # Call Django Rest Framework's default exception handler
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        # Customize the 404 response to return JSON
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    return response
