#!/usr/bin/env python
# -*- coding: utf-8

from twisted.internet import reactor, protocol

from protocol import PluggableBotProto



class BotFactory(protocol.ClientFactory):
    "IRC bot factory"
    protocol = PluggableBotProto

    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        "reconnect"
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
