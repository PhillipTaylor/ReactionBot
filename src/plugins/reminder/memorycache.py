#!/usr/bin/env python
# -*- coding: utf-8


import icache

"""
dummy Cache interface implementation
"""


class MemoryCache(icache.ICache):
    """Cache implementation in memmory"""

    def __init__(self):
        self.cache = {}

    def add(self, key, value):
        if not key in self.cache:
            self.cache[key] = []
        self.cache[key].append(value)
        return value

    def get(self, key):
        if not key in self.cache:
            return None
        value = self.cache[key]
        return value

    def drop(self, key):
        if key in self.cache:
            value = self.cache[key]
            del self.cache[key]
            return value
        return None

