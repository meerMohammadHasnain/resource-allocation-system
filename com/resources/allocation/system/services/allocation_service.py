from com.resources.allocation.system.utils.singleton import SingletonMeta


class AllocateService(object):

    __metaclass__ = SingletonMeta

    def __init__(self, resource_service, task_service, resource_allocation_strategy):
        self.resource_service = resource_service
        self.task_service = task_service
        self.resource_allocation_strategy = resource_allocation_strategy

    def allocate_resources(self, task_request, task_id):
        available_resources = self.resource_service.get_available_resources(
            task_request.data_center_id,
            task_request.resource_type,
            task_request.configuration)
        if len(available_resources) < task_request.quantity:
            print("Not enough resources available for task_id: {}, task_request: {}"
                  .format(task_id, str(task_request)))
            return False
        allocated_resources = self.resource_allocation_strategy.get_allocated_resources(
            task_request, available_resources)
        task = self.task_service.get_task(task_id)
        task.allocate_resources(allocated_resources)
        print("Allocated resources for task_id: {}, task_request: {}, resources: {}".
              format(task_id, str(task_request), allocated_resources))
        return True
