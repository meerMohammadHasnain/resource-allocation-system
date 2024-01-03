import uuid

from com.resources.allocation.system.models.resource import Resource
from com.resources.allocation.system.utils.singleton import SingletonMeta
from com.resources.allocation.system.exceptions.exceptions import DataCenterNotFoundException,\
    ResourceNotFoundException


class ResourceService(object):

    __metaclass__ = SingletonMeta

    def __init__(self, data_center_service, task_service):
        self.data_center_service = data_center_service
        self.task_service = task_service
        self.resources = {}

    def is_exist(self, resource_id):
        return resource_id in self.resources

    def get_resource(self, resource_id):
        if not self.is_exist(resource_id):
            raise ResourceNotFoundException()
        return self.resources[resource_id]

    def add_resource(self, resource_type, data_center_id, configuration, price_per_hour):
        data_center = self.data_center_service.get_data_center(data_center_id)
        if not data_center:
            raise DataCenterNotFoundException()
        resource_id = str(uuid.uuid4())
        resource = Resource(resource_id=resource_id, data_center_id=data_center_id,
                            resource_type=resource_type, configuration=configuration,
                            price_per_hour=price_per_hour)
        self.resources[resource_id] = resource
        data_center.add_resource(resource)
        return resource_id

    def delete_resource(self, resource_id):
        if not self.is_exist(resource_id):
            raise ResourceNotFoundException()
        resource = self.resources.pop(resource_id)
        data_center = self.data_center_service.get_data_center(resource.resource_id)
        data_center.delete_resource(resource_id)

    def get_all_allocated_resources(self, data_center_id, resource_type=None, resource_configuration=None):
        resources = []
        running_tasks = self.task_service.get_all_running_tasks(data_center_id)
        for task in running_tasks:
            for resource in task.allocated_resources:
                if resource_type and resource.resource_type != resource_type:
                    continue
                if resource_configuration and not resource.configuration.is_match(resource_configuration):
                    continue
                resources.append(resource)
        return resources

    def get_available_resources(self, data_center_id, resource_type=None, resource_configuration=None):
        allocated_resources = set(resource.resource_id for resource in
                                  self.get_all_allocated_resources(data_center_id))
        available_resources = []
        for resource_id, resource in self.resources.items():
            if resource_id in allocated_resources:
                continue
            if resource_type and resource.resource_type != resource_type:
                continue
            if resource_configuration and not resource.configuration.is_match(resource_configuration):
                continue
            available_resources.append(resource)
        return available_resources
