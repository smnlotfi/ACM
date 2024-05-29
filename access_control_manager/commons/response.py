from rest_framework.response import Response
from .logger import logger

class APIResponse:
    def __init__(self, data=None):
        self.data = data

    def error(self,message):
        return {
            'error': True,
            'message': message,
        }



    def success(self):
        return {
            'success': True,
            'data': self.data,
        }
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self



def ErrorResponse(status_code,error):
    with APIResponse() as response:
        data=response.error(error)
    logger.error(f"Error {status_code}: {error}")
    return Response(data, status=status_code)
    
def SuccessResponse(status_code,data):
    with APIResponse(data) as response:
        data=response.success()
        logger.info(f"Success {status_code}")
        return Response(data, status=status_code)
