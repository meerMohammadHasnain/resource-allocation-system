
class BaseAPIException(Exception):

    def __init__(self, message):
        super(BaseAPIException, self).__init__(message)

    def __str__(self):
        return str(self.message)


class DataCenterNotFoundException(BaseAPIException):

    def __init__(self, message="Data Center not found"):
        super(DataCenterNotFoundException, self).__init__(message)


class ResourceNotFoundException(BaseAPIException):

    def __init__(self, message="Resource not found"):
        super(ResourceNotFoundException, self).__init__(message)


class TaskNotFoundException(BaseAPIException):

    def __init__(self, message="Task not found"):
        super(TaskNotFoundException, self).__init__(message)
