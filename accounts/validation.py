from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status


class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'

    def __init__(self, detail,status_code=None):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {"status":False,"message": force_str(detail)}
        else: self.detail = {'detail': force_str(self.default_detail)}