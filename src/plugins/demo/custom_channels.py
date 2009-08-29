#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handle messages only from choosen channels
"""


from zope.interface import implements

from core.plugins.manager import plugin_manager
from core.plugins.interface import ICustomChannelsHandler, IActionHandler


class Echo(object):

    implements(ICustomChannelsHandler, IActionHandler)

    def __init__(self, name, accept_channels):
        self.name = 'custom.echo.' + name
        self.channels = frozenset(accept_channels)

    def accepts_channel(self, channel):
        return channel in self.channels

    def accepts_action(self, action):
        return action == 'privmsg'

    def handle_action(self, protocol, action, user, message):
        message = 'ECHO: %s' % message
        return protocol.say(protocol.channel, message)

echo = Echo('custom_echo', ['test_bot_1', 'test_bot_2'])
plugin_manager.register(echo)
