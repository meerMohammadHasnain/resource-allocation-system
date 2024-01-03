from com.resources.allocation.system.utils.singleton import SingletonMeta


class TaskController(object):

    __metaclass__ = SingletonMeta

    def __init__(self, task_service):
        self.task_service = task_service

    def add_task(self, task_request):
        print("Received request, {}".format(str(task_request)))
        return self.task_service.add_task(task_request)
