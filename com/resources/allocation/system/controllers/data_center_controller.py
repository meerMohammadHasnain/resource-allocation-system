from com.resources.allocation.system.utils.singleton import SingletonMeta


class DataCenterController(object):

    __metaclass__ = SingletonMeta

    def __init__(self, data_center_service):
        self.data_center_service = data_center_service

    def add_data_center(self, region):
        return self.data_center_service.create_data_center(region)
