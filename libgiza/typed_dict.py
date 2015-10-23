"""
Provides the basis for a more strictly typed dictionary that ensures all keys
and values will be of a specific type, and will throw exceptions if keys,
values, or pairs of keys and values are of the wrong type or fail validation.
"""

import abc

import future.utils


class TypedDict(future.utils.with_metaclass(abc.ABCMeta, dict)):
    """
    An abstract base class definition that ensures that keys and values are of
    the correct type. Requires users implement ``check_key()``,
    ``check_value()`` and ``check_pair()`` methods that allow the these objects
    to validate input.
    """

    def __init__(self, key_type, value_type):
        errors = []
        if isinstance(key_type, type):
            self.key_type = key_type
        else:
            errors.append("key_type ({0}) is not a type value".format(key_type))

        if isinstance(value_type, type):
            self.value_type = value_type
        else:
            errors.append("value_type ({0}) is not a type value".format(value_type))

        if len(errors) > 0:
            raise TypeError("; ".join(errors))

    def __setitem__(self, key, value):
        type_errors = []
        value_errors = []

        if isinstance(key, self.key_type):
            value_errors.extend(self.check_key(key))
        else:
            try:
                key = self.key_type(key)
            except Exception as e:
                type_errors.append("key {0} ({1}) is not of type {2} (had error "
                                   "{3}:{4})".format(key, type(key), self.key_type, type(e), e))

        if isinstance(value, self.value_type):
            value_errors.extend(self.check_value(value))
        else:
            try:
                value = self.value_type(value)
            except Exception as e:
                type_errors.append("value for key {0} is not of type {1} (is {2}). (had error "
                                   "{3}:{4})".format(key, self.value_type, type(value), type(e), e))

        # if checks for pair errors depend on type/values being correct they
        # may except in unpredictable ways
        try:
            pair_errors = self.check_pair(key, value)
            if len(pair_errors) > 0:
                value_errors.extend(pair_errors)
        except Exception as e:
            value_errors.append("encountered {0} error when validating "
                                "pair for key {1}".format(type(e), key))

        if len(type_errors) > 0:
            # want to report value errors too:
            type_errors.extend(value_errors)
            raise TypeError('; '.join(type_errors))

        if len(value_errors) > 0:
            raise ValueError('; '.join(value_errors))

        dict.__setitem__(self, key, value)

    def ingest(self, args):
        if args is None or len(args) == 0:
            return
        elif isinstance(args, tuple):
            dict.__init__(self, *args)
        else:
            dict.__init__(self, args)

    @abc.abstractmethod
    def check_key(self, key):
        return []

    @abc.abstractmethod
    def check_value(self, value):
        return []

    @abc.abstractmethod
    def check_pair(self, key, value):
        return []
