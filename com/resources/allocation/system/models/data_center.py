from com.resources.allocation.system.models.resource import Resource
from com.resources.allocation.system.utils.document import Document
from com.resources.allocation.system.utils.property import DictType, StringType


class DataCenter(Document):
    data_center_id = StringType(is_mandatory=True)
    region = StringType(is_mandatory=True)
    resources = DictType(key_type=StringType, value_type=Resource, default={})

    def add_resource(self, resource):
        self.resources[resource.resource_id] = resource

    def delete_resource(self, resource_id):
        self.resources.pop(resource_id)
