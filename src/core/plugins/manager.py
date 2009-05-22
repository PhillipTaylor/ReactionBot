#!/usr/bin/env python
# -*- coding: utf-8

from twisted.internet.task import LoopingCall

from core.plugins.interface import IPlugin, IActionHandler, IPeriodic
from core.plugins.interface import ICustomChannelsHandler


def _filter_interface(plugins, interface):
    return filter(lambda p: interface.providedBy(p), plugins)

def _filter_action(plugins, action):
    """Returns list of plugins that should handle given action."""
    plugins = _filter_interface(plugins, IActionHandler)
    return filter(lambda p: p.accepts_action(action), plugins)

def _filter_channel(plugins, channel):
    """Returns list of plugins that should handle action on given channel.

    If plugin does not implement ICustomChannelsHandler, it means it should
    handle signals from all channels.
    """
    f_plugins = []
    for p in plugins:
        if ICustomChannelsHandler.providedBy(p):
            if p.accepts_channel(channel):
                f_plugins.append(p)
        else:
            f_plugins.append(p)
    return f_plugins

def _filter_name(plugins, name):
    return filter(lambda p: p.name == name, plugins)


class PlugginManager(object):
    """Singleton plugin manager"""
    __instance = None

    def __new__(cls):
        """Keep this class singleton"""
        if not PlugginManager.__instance:
            PlugginManager.__instance = object.__new__(cls)
        return PlugginManager.__instance

    def __init__(self):
        self._plugins = []

    def register(self, plugin):
        """Register new object, that implements IPlugin interface."""
        if not IPlugin.providedBy(plugin):
            raise TypeError("Plugin interface not implemented by %s" % plugin)
        self._plugins.append(plugin)

    def filter(self, action=None, channel=None, interface=None, name=None):
        """Returns list of plugins, filtered by given arguments."""
        plugins = self._plugins
        if interface:
            plugins = _filter_interface(plugins, interface)
        if action:
            plugins = _filter_action(plugins, action)
        if channel:
            plugins = _filter_channel(plugins, channel)
        if name:
            plugins = _filter_name(plugins, name)
        return plugins

    def start_periodics(self):
        for periodic in self.filter(interface=IPeriodic):
            if hasattr(periodic, "loop"):
                continue
            p = LoopingCall(periodic.periodic_handler, protocol_manager)
            periodic.loop = p
            p.start(periodic.sleep_time)


plugin_manager = PlugginManager()


class ProtocolManager(list):
    def register(self, protocol):
        self.append(protocol)

    def filter(self, channels=None):
        protocols = self
        if channels:
            protocols = filter(lambda p: p.channel in channels, protocols)
        return protocols

    def unregister(self, protocol):
        self.remove(protocol)


protocol_manager = ProtocolManager()
