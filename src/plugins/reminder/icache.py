#!/usr/bin/env python
# -*- coding: utf-8

"""
Cache interface module
"""


class ICache(object):
    "Cache intefrace"

    def add(self, key, value):
        """If key does not exist, create new one and set value. Else, add value
        to existing data.
        """

    def get(self, key):
        """Returns key value or None if key does not exist."""

    def drop(self, key):
        """Delete key value"""
