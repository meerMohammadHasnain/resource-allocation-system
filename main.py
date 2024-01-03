from com.resources.allocation.system.controllers.data_center_controller import DataCenterController
from com.resources.allocation.system.controllers.resource_controller import ResourceController
from com.resources.allocation.system.controllers.task_controller import TaskController

from com.resources.allocation.system.services.data_center_service import DataCenterService
from com.resources.allocation.system.services.resource_service import ResourceService
from com.resources.allocation.system.services.task_service import TaskService
from com.resources.allocation.system.services.queue_service import QueueService
from com.resources.allocation.system.services.allocation_service import AllocateService

from com.resources.allocation.system.strategy.best_execution_time_resource_allocation_strategy import BestExecutionTimeResourceAllocationStrategy

from com.resources.allocation.system.models.resource import ResourceConfiguration
from com.resources.allocation.system.requests.task_request import TaskRequest

from com.resources.allocation.system.enums.resource_type import ResourceType

from com.resources.allocation.system.workers.task_executor import TaskExecutor

data_center_service = DataCenterService()
queue_service = QueueService()
task_service = TaskService(data_center_service, queue_service)
resource_service = ResourceService(data_center_service, task_service)
best_execution_time_resource_allocation_strategy = BestExecutionTimeResourceAllocationStrategy()
allocation_service = AllocateService(resource_service, task_service, best_execution_time_resource_allocation_strategy)

data_center_controller = DataCenterController(data_center_service)
resource_controller = ResourceController(resource_service)
task_controller = TaskController(task_service)


data_center_1 = data_center_controller.add_data_center("us-east-1")

resource_1 = resource_controller.add_resource(
    ResourceType.SERVER_INSTANCE, data_center_1, ResourceConfiguration(cpu_cores=8), 100)
resource_2 = resource_controller.add_resource(
    ResourceType.SERVER_INSTANCE, data_center_1, ResourceConfiguration(cpu_cores=6), 150)
resource_3 = resource_controller.add_resource(
    ResourceType.SERVER_INSTANCE, data_center_1, ResourceConfiguration(cpu_cores=4), 200)
resource_4 = resource_controller.add_resource(
    ResourceType.SERVER_INSTANCE, data_center_1, ResourceConfiguration(cpu_cores=2), 120)
resource_5 = resource_controller.add_resource(
    ResourceType.SERVER_INSTANCE, data_center_1, ResourceConfiguration(cpu_cores=2), 90)

task_request_1 = TaskRequest(data_center_id=data_center_1, resource_type=ResourceType.SERVER_INSTANCE,
                             quantity=2, configuration=ResourceConfiguration(cpu_cores=3),
                             duration_in_hours=0.0004)
task_request_2 = TaskRequest(data_center_id=data_center_1, resource_type=ResourceType.SERVER_INSTANCE,
                             quantity=1, configuration=ResourceConfiguration(cpu_cores=6),
                             duration_in_hours=0.0004)
task_request_3 = TaskRequest(data_center_id=data_center_1, resource_type=ResourceType.SERVER_INSTANCE,
                             quantity=3, configuration=ResourceConfiguration(cpu_cores=2),
                             duration_in_hours=0.0002)
task_request_4 = TaskRequest(data_center_id=data_center_1, resource_type=ResourceType.SERVER_INSTANCE,
                             quantity=2, configuration=ResourceConfiguration(cpu_cores=2),
                             duration_in_hours=0.0002)

task_executor = TaskExecutor(data_center_1, queue_service, allocation_service)

task_executor.start()

task_1 = task_controller.add_task(task_request_1)

task_2 = task_controller.add_task(task_request_2)

task_3 = task_controller.add_task(task_request_3)

task_4 = task_controller.add_task(task_request_4)
