class PyCAIError(Exception):
    ...


class UnknownError(PyCAIError):
    ...


class RequestError(PyCAIError):
    ...


class SessionClosedError(RequestError):
    ...


class ServerError(PyCAIError):
    ...


class AuthenticationError(PyCAIError):
    ...


class InvalidArgumentError(PyCAIError):
    ...


class ActionError(PyCAIError):
    ...


class FetchError(ActionError):
    ...


class SearchError(ActionError):
    ...


class CreateError(ActionError):
    ...


class SetError(ActionError):
    ...


class UpdateError(ActionError):
    ...


class EditError(ActionError):
    ...


class DeleteError(ActionError):
    ...


class UploadError(ActionError):
    ...
