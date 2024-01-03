from com.resources.allocation.system.strategy.resource_allocation_strategy import ResourceAllocationStrategy


class LeastPriceResourceAllocationStrategy(ResourceAllocationStrategy):

    def __init__(self):
        super(LeastPriceResourceAllocationStrategy, self).__init__()

    def get_allocated_resources(self, request, resources):
        resources.sort(key=lambda res: res.price_per_hour)
        return resources[:request.quantity]
