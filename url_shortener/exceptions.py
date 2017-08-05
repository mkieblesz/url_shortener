class ErrorException(Exception):
    '''Base Exception class for error responses'''
    status = None
    message = None

    def __init__(self, msg=None, status=None):
        if msg is not None:
            self.message = msg
        if status is not None:
            self.status = status

    def is_error(self):
        return self.status >= 500

    def get_response(self):
        return {
            'error': {
                'message': self.message
            }
        }


class UncategorisedException(ErrorException):
    '''Exception thrown for unknown HTTPExceptions that may occur'''
    status = 500
    message = 'Unrecognized exception'


class UrlValidationException(ErrorException):
    status = 400
    message = 'Provided url is not valid'


class BadRequestFormatException(ErrorException):
    status = 415
    message = 'Unsupported request format'


class NotFoundException(ErrorException):
    status = 404
    message = 'Not found'
