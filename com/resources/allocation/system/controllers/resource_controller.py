from com.resources.allocation.system.utils.singleton import SingletonMeta


class ResourceController(object):

    __metaclass__ = SingletonMeta

    def __init__(self, resource_service):
        self.resource_service = resource_service

    def add_resource(self, resource_type, data_center_id, configuration, price_per_hour):
        return self.resource_service.add_resource(resource_type, data_center_id,
                                                  configuration, price_per_hour)

    def delete_resource(self, resource_id):
        self.resource_service.delete_resource(resource_id)

    def get_available_resources(self, data_center_id, resource_type, resource_configuration):
        return self.resource_service.get_available_resources(data_center_id, resource_type, resource_configuration)

    def get_allocated_resources(self, data_center_id, resource_type):
        return self.resource_service.get_all_allocated_resources(data_center_id, resource_type)
