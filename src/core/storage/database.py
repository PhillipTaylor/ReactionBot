# -*- coding: utf-8

import pickle
import os

import settings


DUMP_FILE = getattr(settings, "DUMP_FILE", "dump_file.pickle")


class FileStorage(object):
    """Pickle and store data in file.. sooo cool!"""
    __instance = None

    def __new__(type):
        if not FileStorage.__instance:
            FileStorage.__instance = object.__new__(type)
        return FileStorage.__instance

    def __init__(self):
        self.data = {}

    def get(self, key):
        """Get data or None if does not exist"""
        if not key in self.data:
            return None
        return self.data[key]

    def set(self, key, value):
        """Override data if allready exists"""
        self.data[key] = value

    def dump(self):
        data = pickle.dumps(self.data)
        with open(DUMP_FILE, "wb") as dump_file:
            dump_file.write(data)

    def load(self):
        try:
            with open(DUMP_FILE, "rb") as dump_file:
                self.data = pickle.loads(dump_file.read())
        except IOError:
            return {}
