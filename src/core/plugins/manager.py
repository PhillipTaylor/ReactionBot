#!/usr/bin/env python
# -*- coding: utf-8


from twisted.internet import task
from core.storage.database import FileStorage


class MultiHandler(object):
    """Single action handler

    Can call any number of handlers at single call
    """
    def __init__(self, manager, action):
        self.manager = manager
        self.action = action
        self._handlers = {'__all__' : []}

    def add(self, handler, channels=None):
        if not channels:
            channels = ["__all__", ]
        for channel in channels:
            if not channel in self._handlers:
                self._handlers[channel] = []
            self._handlers[channel].append(handler)
        return self

    def __call__(self, protocol, *args, **kwds):
        channel = protocol.channel
        for h in self._handlers['__all__']:
            h(protocol=protocol, *args, **kwds)
        if channel in self._handlers:
            for h in self._handlers[channel]:
                h(protocol=protocol, *args, **kwds)

    def get_handlers(self):
        handlers = []
        for c in self._handlers:
            handlers.extend(self._handlers[c])
        return handlers



class PlugginManager(object):
    """Plugin manager singleton"""
    __instance = False

    def __init__(self):
        if self.__instance:
            return self.__instance
        self.__instance = self
        self._storable_plugins = []
        self.action_handlers = {}
        self.periodic_actions = []
        self.protocols = []

    def register_action(self, action, handler, channels=None):
        "register new action handlers"
        if not action in self.action_handlers:
            self.action_handlers[action] = MultiHandler(self, action)
        return self.action_handlers[action].add(handler, channels)

    def get_handler(self, action):
        "returns list of handlers for given action"
        if not action in self.action_handlers:
            return None
        return self.action_handlers[action]


    def register_periodic(self, handler, period, channels=None):
        """Collect all periodic actions, but do not run them untill some
        protocol instances will be set
        """
        self.periodic_actions.append((handler, period, channels))

    def start_periodics(self):
        "call handler each `period` seconds"
        for (handler, period, channels) in self.periodic_actions:
            if not channels:
                handler.protocols = self.protocols[:]
            else:
                handler.protocols = filter(
                        lambda p: p.channel in channels, self.protocols)
            periodic = task.LoopingCall(handler)
            periodic.start(period)

    def register_storable(self, loader, dumper, id):
        self._storable_plugins.append({
            'loader': loader,
            'dumper': dumper,
            'id': id,
            })

    def plugins_initialize(self):
        db = FileStorage()
        db.load()
        for p in self._storable_plugins:
            p['loader'](db.get(p['id']))

    def plugins_finalize(self):
        "finalize plugins"
        db = FileStorage()
        for p in self._storable_plugins:
            db.set(p['id'], p['dumper']())
        db.dump()


plugin_manager = PlugginManager()
