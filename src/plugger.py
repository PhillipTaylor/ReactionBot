#!/usr/bin/env python
# -*- coding: utf-8


class MultiHandler(object):
    """Single action handler

    Can call any number of handlers at single call
    """
    def __init__(self, manager, action, handlers=None):
        self.manager = manager
        self.action = action
        self._handlers = handlers or []

    def add(self, *handlers):
        self._handlers.extend(handlers)
        return self

    def __call__(self, *args, **kwds):
        if not 'protocol' in kwds:
            kwds['protocol'] = self.manager.protocol
        for h in self._handlers:
            h(*args, **kwds)



class PlugginManager(object):
    """Plugin manager singleton"""
    __instance = False

    def __init__(self):
        if self.__instance:
            return self.__instance
        self.__instance = self
        self.action_handlers = {}
        protocol = None

    def register(self, action, *handlers):
        "register new action handlers"
        if not action in self.action_handlers:
            self.action_handlers[action] = MultiHandler(self, action)
        return self.action_handlers[action].add(*handlers)

    def get_handler(self, action):
        "returns list of handlers for given action"
        if not action in self.action_handlers:
            return None
        return self.action_handlers[action]


plugg_manager = PlugginManager()