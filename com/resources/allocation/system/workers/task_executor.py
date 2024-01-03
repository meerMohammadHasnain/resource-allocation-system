import time

from threading import Thread


class TaskExecutor(Thread):

    def __init__(self, data_center_id, queue_service, allocation_service, interval=1):
        self.interval = interval
        self.data_center_id = data_center_id
        self.queue_service = queue_service
        self.allocation_service = allocation_service
        super(TaskExecutor, self).__init__()

    def run(self):
        while True:
            self._poll_and_execute_tasks()
            time.sleep(self.interval)

    def _poll_and_execute_tasks(self):
        print("Polling task for Data Center: {}".format(self.data_center_id))
        task_request, task_id = self.queue_service.poll_task(self.data_center_id)
        if task_request:
            if not self.allocation_service.allocate_resources(task_request, task_id):
                self.queue_service.enqueue_task(task_request, task_id)
                print("Queueing back task_id: {}, task_request: {}".format(task_id, str(task_request)))
