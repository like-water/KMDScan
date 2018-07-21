#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict


class linq_list(list):
    def __init__(self, iterable):
        self.iterable = iterable

    def group_by(self, keyfunc):
        rel = {}
        for item in self.iterable:
            if keyfunc(item) not in rel:
                rel[keyfunc(item)] = []

            rel[keyfunc(item)].append(item)
        return linq_dict(rel)

    def first_or_default(self, default_value=None):
        return self.iterable[0] if self.iterable else default_value

    def select(self, selectfunc=None):
        if selectfunc:
            return [selectfunc(item) for item in self.iterable]
        else:
            return self.iterable

    def where(self, filterfunc):
        return linq_list(filter(filterfunc, self.iterable))

    def order_by(self, sorted_func=None, sorted_key_func=None, reverse=False):
        return linq_list(sorted(self.iterable, cmp=sorted_func, key=sorted_key_func, reverse=reverse))

    def count(self):
        return self.iterable.__len__()

    def __str__(self):
        return self.iterable

    def __add__(self, other):
        return linq_list(self.iterable + other.iterable)

    def __iadd__(self, other):
        self.iterable += other.iterable


class linq_dict(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __str__(self):
        return self.iterable

    def select(self, kvfunc=None, vfunc=None):
        if kvfunc:
            return dict([kvfunc(k, v) for k, v in self.iterable.items()])
        elif vfunc:
            return {k: vfunc(v) for k, v in self.iterable.items()}
        else:
            return self.iterable

    def order_by(self, sorted_func=None, sorted_key_func=None, reverse=False):
        return linq_dict(
            OrderedDict(sorted(self.iterable.items(), cmp=sorted_func, key=sorted_key_func, reverse=reverse)))

    def where(self, filterfunc):
        return linq_dict({ k:v for k,v in self.iterable.items() if filterfunc(k,v)})

    def __add__(self, other):
        return linq_dict(dict(self.iterable, **other.iterable))

    def __iadd__(self, other):
        return self.iterable.update(other.iterable)
