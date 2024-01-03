from datetime import datetime, timedelta
from com.resources.allocation.system.enums.task_status import TaskStatus
from com.resources.allocation.system.models.resource import Resource
from com.resources.allocation.system.utils.document import Document
from com.resources.allocation.system.utils.property import DocumentType, DateTimeType, ListType, FloatType, EnumType, StringType


class Task(Document):
    task_id = StringType(is_mandatory=True)
    start_time = DateTimeType()
    end_time = DateTimeType()
    duration_in_hours = FloatType(is_mandatory=True)
    allocated_resources = ListType(entity_type=Resource, default=[])
    data_center_id = StringType(is_mandatory=True)
    status = EnumType(enum_class=TaskStatus, default=TaskStatus.CREATED)

    def is_completed(self):
        if self.status == TaskStatus.RUNNING and \
                datetime.utcnow() > self.start_time + timedelta(hours=self.duration_in_hours):
            self.status = TaskStatus.COMPLETED
            self.end_time = self.start_time + timedelta(hours=self.duration_in_hours)
        return self.status == TaskStatus.COMPLETED

    def allocate_resources(self, resources):
        self.allocated_resources = resources
        self.status = TaskStatus.RUNNING
        self.start_time = datetime.utcnow()
