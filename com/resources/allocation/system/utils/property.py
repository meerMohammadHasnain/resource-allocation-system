from copy import deepcopy
from datetime import datetime
from dateutil import parser
from enum import Enum


class BaseType(object):

    def __init__(self, is_mandatory=False, default=None):
        self.is_mandatory = is_mandatory
        self.default = default

    def validate(self, value):
        if self.is_mandatory and value is None:
            raise ValueError('Missing mandatory field')
        if self.default is not None and value is None:
            return deepcopy(self.default)
        return value


class StringType(BaseType):

    def __init__(self, is_mandatory=False, default=None):
        super(StringType, self).__init__(is_mandatory=is_mandatory, default=default)

    def validate(self, value):
        value = super(StringType, self).validate(value)
        if value is not None and not isinstance(value, str) and not isinstance(value, unicode):
            raise TypeError('Invalid string type')
        return value


class IntegerType(BaseType):

    def __init__(self, is_mandatory=False, min_value=None, max_value=None, default=None):
        super(IntegerType, self).__init__(is_mandatory=is_mandatory, default=default)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        value = super(IntegerType, self).validate(value)
        if value is not None and not isinstance(value, int) and not isinstance(value, long):
            raise TypeError('Invalid integer type')
        if self.min_value is not None or self.max_value is not None:
            self.__validate_bounds(value)
        return value

    def __validate_bounds(self, value):
        if (self.min_value is not None and value < self.min_value) \
                or (self.max_value is not None and value > self.max_value):
            raise ValueError('Invalid value, bounds breached')


class FloatType(BaseType):

    def __init__(self, is_mandatory=False, default=None):
        super(FloatType, self).__init__(is_mandatory=is_mandatory)

    def validate(self, value):
        value = super(FloatType, self).validate(value)
        if value is not None and not isinstance(value, float):
            raise TypeError('Invalid float type')
        return value


class DateTimeType(BaseType):

    def __init__(self, is_mandatory=False, default=None):
        super(DateTimeType, self).__init__(is_mandatory=is_mandatory, default=default)

    def validate(self, value):
        value = super(DateTimeType, self).validate(value)
        if value is not None and not isinstance(value, datetime):
            try:
                return parser.parse(value, ignoretz=True)
            except ValueError:
                raise TypeError('Invalid datetime type')
        return value


class EnumType(BaseType):

    def __init__(self, enum_class, is_mandatory=False, default=None):
        super(EnumType, self).__init__(is_mandatory=is_mandatory, default=default)
        if not issubclass(enum_class, Enum) or not hasattr(enum_class, 'map'):
            raise TypeError('Invalid enum type')
        self.enum_class = enum_class

    def validate(self, value):
        value = super(EnumType, self).validate(value)
        if value is not None:
            if self.enum_class.map().get(str(value)) is None:
                raise ValueError('Invalid enum value')
        return value


class ListType(BaseType):

    def __init__(self, entity_type=object, is_mandatory=False, default=None):
        super(ListType, self).__init__(is_mandatory=is_mandatory, default=default)
        self.entity_type = entity_type

    def validate(self, value):
        value = super(ListType, self).validate(value)
        if value is not None and not isinstance(value, list):
            raise TypeError('Invalid list type')
        if any(not isinstance(entity, self.entity_type) for entity in value):
            raise TypeError('Invalid type of element in list type')
        return value


class DictType(BaseType):

    def __init__(self, key_type=object, value_type=object, is_mandatory=False, default=None):
        super(DictType, self).__init__(is_mandatory=is_mandatory, default=default)
        self.key_type = key_type
        self.value_type = value_type

    def validate(self, value):
        value = super(DictType, self).validate(value)
        if value is not None and not isinstance(value, dict):
            raise TypeError('Invalid dict type')
        if any(not isinstance(k, self.key_type) or not isinstance(v, self.value_type)
               for k, v in value.items()):
            raise TypeError('Invalid type of key/ value in dict type')
        return value


class DocumentType(BaseType):

    def __init__(self, document, is_mandatory=False, default=None):
        super(DocumentType, self).__init__(is_mandatory=is_mandatory, default=default)
        from com.resources.allocation.system.utils.document import Document
        if not issubclass(document, Document):
            raise TypeError('Invalid document type')
        self.document = document

    def validate(self, value):
        value = super(DocumentType, self).validate(value)
        from com.resources.allocation.system.utils.document import Document
        if isinstance(value, Document):
            value = value.to_dict()
        if value is not None:
            try:
                return self.document(**value)
            except Exception as ex:
                raise ValueError('Incompatible document schema, error: %s' % str(ex))
