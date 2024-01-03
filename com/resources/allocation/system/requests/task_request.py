from com.resources.allocation.system.enums.resource_type import ResourceType
from com.resources.allocation.system.models.resource import ResourceConfiguration
from com.resources.allocation.system.utils.document import Document
from com.resources.allocation.system.utils.property import DocumentType, IntegerType, FloatType, \
    EnumType, StringType


class TaskRequest(Document):
    data_center_id = StringType(is_mandatory=True)
    resource_type = EnumType(enum_class=ResourceType)
    quantity = IntegerType(min_value=1, default=1)
    configuration = DocumentType(document=ResourceConfiguration)
    duration_in_hours = FloatType(is_mandatory=True)
