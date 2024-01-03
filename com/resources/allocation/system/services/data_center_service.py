import uuid

from com.resources.allocation.system.models.data_center import DataCenter
from com.resources.allocation.system.utils.singleton import SingletonMeta
from com.resources.allocation.system.exceptions.exceptions import DataCenterNotFoundException


class DataCenterService(object):

    __metaclass__ = SingletonMeta

    def __init__(self):
        self.data_centers = {}

    def get_data_center(self, data_center_id):
        if data_center_id not in self.data_centers:
            raise DataCenterNotFoundException()
        return self.data_centers[data_center_id]

    def create_data_center(self, region):
        data_center_id = str(uuid.uuid4())
        data_center = DataCenter(data_center_id=data_center_id, region=region)
        self.data_centers[data_center_id] = data_center
        return data_center_id
