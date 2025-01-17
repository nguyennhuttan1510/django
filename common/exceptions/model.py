from rest_framework.exceptions import APIException


class ResponseBase:
    def __init__(self, data=None, message=None, status=None):
        self.data = data
        self.message = message
        self.status = status

    def get(self):
        result = lambda: None
        if self.message:
            result.message = self.message
        if self.status:
            result.status = self.status
        result.data = self.data
        return result.__dict__
        # return {
        #     'message': self.message,
        #     'data': self.data
        # }

    def __str__(self):
        return self


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
