# -*- coding: utf-8 -*-
from requests import HTTPError

__docformat__ = 'reStructuredText'


class MissingAccessTokenException(IOError):
    pass


class ConnectionOperationTimeoutException(IOError):
    def __init__(self, *args, **kwargs):
        """
        An connection operation took too long to perform
        :param Connection connection: the connection
        """
        self.connection = kwargs.pop('connection', None)
        super(ConnectionOperationTimeoutException, self).__init__(*args, **kwargs)


class ConnectionOperationFailedException(IOError):
    def __init__(self, *args, **kwargs):
        """
        An connection operation failed to perform
        :param Connection connection: the connection
        """
        self.connection = kwargs.pop('connection', None)
        super(ConnectionOperationFailedException, self).__init__(*args, **kwargs)


class ClientHttpException(IOError):
    def __init__(self, *args, **kwargs):
        """
        An exception representing a bad http call from the client
        :param int code: the http status code
        :param str message: the message describing the issue
        :param requests.Response response: the response object returned from the Http library
        """
        self.status_code = kwargs.pop('status_code', None)
        self.response = kwargs.pop('response', None)
        super(ClientHttpException, self).__init__(*args, **kwargs)


class BadRequestException(ClientHttpException):
    """400"""
    pass


class UnauthorizedException(ClientHttpException):
    """401"""
    pass


class PaymentRequiredException(ClientHttpException):
    """402"""
    pass


class ForbiddenException(ClientHttpException):
    """403"""
    pass


class NotFoundException(ClientHttpException):
    """404"""
    pass


class MethodNotAllowedException(ClientHttpException):
    """405"""
    pass


class RequestTimeoutException(ClientHttpException):
    """408"""
    pass


class ConflictException(ClientHttpException):
    """409"""
    pass


class PayloadTooLargeException(ClientHttpException):
    """413"""
    pass


class UriTooLongException(ClientHttpException):
    """414"""
    pass


class UnsupportedMediaTypeException(ClientHttpException):
    """415"""
    pass


class UnprocessableEntityException(ClientHttpException):
    """422"""
    pass


class InternalServerErrorException(ClientHttpException):
    """500"""
    pass


class NotImplementedException(ClientHttpException):
    """501"""
    pass


class BadGatewayException(ClientHttpException):
    """502"""
    pass


class ServiceUnavailableException(ClientHttpException):
    """503"""
    pass


__ERROR_EXCEPTION_CLASSES = {
    400: BadRequestException,
    401: UnauthorizedException,
    402: PaymentRequiredException,
    403: ForbiddenException,
    404: NotFoundException,
    405: MethodNotAllowedException,
    408: RequestTimeoutException,
    409: ConflictException,
    413: PayloadTooLargeException,
    414: UriTooLongException,
    415: UnsupportedMediaTypeException,
    422: UnprocessableEntityException,
    500: InternalServerErrorException,
    501: NotImplementedException,
    502: BadGatewayException,
    503: ServiceUnavailableException
}


def raise_response_exception(response):
    """
    Throw the correct exception for the error code given
    :param requests.Response response: the requests response
    :raises: ClientHttpException
    """
    try:
        response.raise_for_status()
    except HTTPError as e:
        exception_class = __ERROR_EXCEPTION_CLASSES.get(response.status_code, ClientHttpException)
        raise exception_class(*e.args, status_code=e.response.status_code, response=e.response)
