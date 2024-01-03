import uuid

from com.resources.allocation.system.models.task import Task
from com.resources.allocation.system.enums.task_status import TaskStatus
from com.resources.allocation.system.utils.singleton import SingletonMeta
from com.resources.allocation.system.exceptions.exceptions import DataCenterNotFoundException, \
    TaskNotFoundException


class TaskService(object):

    __metaclass__ = SingletonMeta

    def __init__(self, data_center_service, queue_service):
        self.data_center_service = data_center_service
        self.queue_service = queue_service
        self.tasks = {}

    def get_task(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundException()
        return self.tasks[task_id]

    def add_task(self, task_request):
        data_center = self.data_center_service.get_data_center(task_request.data_center_id)
        if not data_center:
            raise DataCenterNotFoundException()
        task_id = str(uuid.uuid4())
        task = Task(task_id=task_id, data_center_id= task_request.data_center_id,
                    duration_in_hours=task_request.duration_in_hours)
        self.tasks[task_id] = task
        self.queue_service.enqueue_task(task_request, task_id)
        return task_id

    def get_all_running_tasks(self, data_center_id):
        for task in self.tasks.values():
            if task.data_center_id == data_center_id and not task.is_completed() \
                    and task.status != TaskStatus.CREATED:
                yield task
