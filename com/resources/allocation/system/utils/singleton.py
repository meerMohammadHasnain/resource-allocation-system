import threading


class SingletonMeta(type):

    _instances = {}
    _instance_lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        with cls._instance_lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
