#!/usr/bin/env python
# -*- coding: utf-8 -*-

def _get_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError('{0} is not a valid integer'.format(value))


class json_dict(object):
    __name__ = "json_dict"

    def __init__(self, keys=[]):
        self.keys = keys

    def __call__(self, value):
        for key in self.keys:
            if not value.has_key(key):
                raise ValueError("required parameter missing '%s'" % key)
        return value


class int_min(object):
    __name__ = "int_min"

    def __init__(self, min_num):
        self.min_num = min_num

    def __call__(self, value):
        value = _get_integer(value)
        if value < self.min_num:
            raise ValueError("Invalid argument: {0}. argument must above {1}".format(value, self.min_num))
        return value
