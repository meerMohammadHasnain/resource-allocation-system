from datetime import datetime
from com.resources.allocation.system.utils.property import BaseType


class DocumentMeta(type):

    def __init__(cls, name, bases, class_dict):
        super(DocumentMeta, cls).__init__(cls, bases, class_dict)
        cls._schema = {k: v for k, v in class_dict.items() if isinstance(v, BaseType)}


class Document(object):

    """
    A utility class for performing basic validations
    on the fields of a document when it is created
    """

    __metaclass__ = DocumentMeta

    def __init__(self, **kwargs):
        super(Document, self).__init__()
        for field, schema in self._schema.items():
            value = kwargs.pop(field, None)
            self.__setattr__(field, value)
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        schema = self._schema.get(key)
        if schema:
            try:
                value = schema.validate(value)
            except TypeError as ex:
                raise TypeError('Type mismatch in document field, error: %s' % str(ex))
        super(Document, self).__setattr__(key, value)

    def to_dict(self):

        def serialize(value):
            serialized_value = value
            if isinstance(value, Document):
                serialized_value = value.to_dict()
            if isinstance(value, datetime):
                serialized_value = value.strftime(format='%Y-%m-%dT%H:%M:%SZ')
            if isinstance(value, dict):
                serialized_value = {k: serialize(val) for k, val in value.items()}
            if isinstance(value, list):
                serialized_value = [serialize(item) for item in value]
            return serialized_value

        return {k: serialize(v) for k, v in self.__dict__.items() if v is not None}

    def __str__(self):
        return str(self.to_dict())
