from com.resources.allocation.system.strategy.resource_allocation_strategy import ResourceAllocationStrategy


class BestExecutionTimeResourceAllocationStrategy(ResourceAllocationStrategy):

    def __init__(self):
        super(BestExecutionTimeResourceAllocationStrategy, self).__init__()

    def get_allocated_resources(self, request, resources):
        resources.sort(key=lambda res: res.configuration.cpu_cores, reverse=True)
        return resources[:request.quantity]
