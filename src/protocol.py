#!/usr/bin/env python
# -*- coding: utf-8


from twisted.words.protocols import irc

from core.plugins.manager import plugin_manager


"""
more info:
  http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
"""


class PluggableBotProto(irc.IRCClient):
    def __init__(self):
        plugin_manager.protocols.append(self)

    def signedOn(self):
        "called when succesfully signed on to server"
        self.join(self.factory.channel)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def handleCommand(self, command, prefix, params):
        plugin_handler = plugin_manager.get_handler(command.lower())
        if plugin_handler:
            channel, message = params[:2]
            plugin_handler(protocol=self, user=prefix, \
                    channel=channel, message=message, *params[2:])
        irc.IRCClient.handleCommand(self, command, prefix, params)

    @property
    def nickname(self):
        return self.factory.nickname

    @property
    def channel(self):
        return self.factory.channel
