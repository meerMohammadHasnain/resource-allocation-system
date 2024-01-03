from com.resources.allocation.system.enums.resource_type import ResourceType
from com.resources.allocation.system.utils.document import Document
from com.resources.allocation.system.utils.property import DocumentType, IntegerType, EnumType, StringType


class ResourceConfiguration(Document):
    cpu_cores = IntegerType()
    memory_in_gb = IntegerType()
    storage_in_gb = IntegerType()

    def is_match(self, other):
        if other.cpu_cores and other.cpu_cores > self.cpu_cores:
            return False
        if other.memory_in_gb and other.memory_in_gb > self.memory_in_gb:
            return False
        if other.storage_in_gb and other.storage_in_gb > self.storage_in_gb:
            return False
        return True


class Resource(Document):
    resource_id = StringType(is_mandatory=True)
    data_center_id = StringType(is_mandatory=True)
    resource_type = EnumType(enum_class=ResourceType, is_mandatory=True)
    configuration = DocumentType(document=ResourceConfiguration)
    price_per_hour = IntegerType(is_mandatory=True)
