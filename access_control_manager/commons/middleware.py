from django.conf import settings
from .models import AbstractModel


def RequestExposerMiddleware(get_response):
    def middleware(request):
        AbstractModel.exposed_request = request
        response = get_response(request)
        return response


    return middleware
