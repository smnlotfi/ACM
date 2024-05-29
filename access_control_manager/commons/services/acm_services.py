import requests
from django.conf import settings

API_KEY = settings.COMMONS_APP_SETTINGS["API_KEY"]
ACM_BASE_URL = settings.COMMONS_APP_SETTINGS["ACM_BASE_URL"]
if not ACM_BASE_URL.endswith("/"):
    ACM_BASE_URL += "/"


class ACMService:
    @staticmethod
    def get_user_permissions(user_id):
        response = requests.get(url=f'{ACM_BASE_URL}/user-group/get_all_permissions',
                                params={'user_id': user_id},
                                headers=
                                {
                                    'X-Api-Key': API_KEY
                                })
        if response.status_code == 200:
            return response.json().get("data", {})

    @staticmethod
    def has_user_model_permission(request, model_name, access):
        # if on develop or test environment skip check permission
        if settings.DEBUG:
            return True
        user_id = request.user.id
        if not user_id:
            api_key = request.headers.get('X-Api-Key', None)
            if api_key:
                return True
            return False
        response = requests.get(url=f'{ACM_BASE_URL}user-group/get_model_permissions/',
                                params={'user_id': user_id, 'model_name': model_name},
                                headers=
                                {
                                    'X-Api-Key': API_KEY
                                })

        if response.status_code == 200:
            response = response.json().get("data", {})
            for permission in response:
                if permission.get("access") == access.upper():
                    return True
            return False
        elif response.status_code == 404:
            return True
        elif response.status_code == 400:
            return True
