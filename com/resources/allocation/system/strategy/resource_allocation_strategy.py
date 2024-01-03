from com.resources.allocation.system.utils.singleton import SingletonMeta


class ResourceAllocationStrategy(object):

    __metaclass__ = SingletonMeta

    def get_allocated_resources(self, request, resources):
        raise NotImplementedError
