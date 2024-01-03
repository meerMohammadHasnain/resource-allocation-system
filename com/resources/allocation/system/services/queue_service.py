import threading

from com.resources.allocation.system.utils.singleton import SingletonMeta


class QueueService(object):

    __metaclass__ = SingletonMeta

    def __init__(self):
        self.task_queues = {}

    def get_or_create_queue(self, data_center_id):
        with threading.RLock():
            if data_center_id not in self.task_queues:
                self.task_queues[data_center_id] = []
        return self.task_queues[data_center_id]

    def enqueue_task(self, task_request, task_id):
        with threading.RLock():
            self.get_or_create_queue(task_request.data_center_id).append((task_request, task_id))
            print("Task request queued, , task_id: {}, task_request: {}".format(task_id, str(task_request)))

    def poll_task(self, data_center_id):
        with threading.RLock():
            if data_center_id in self.task_queues and len(self.task_queues[data_center_id]) > 0:
                task_request, task_id = self.task_queues[data_center_id].pop(0)
                print("Task polled, task_id: {}, task_request: {}".format(task_id, str(task_request)))
                return task_request, task_id
            return None, None
