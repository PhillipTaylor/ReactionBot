#!/usr/bin/env python
# -*- coding: utf-8

import optparse

from twisted.internet import reactor

from factory import BotFactory
import settings


def import_plugins():
    for plug in settings.PLUGINS:
        __import__(plug)

def run_server():
    for (server, port, channel, nickname) in settings.CONNECTIONS:
        factory = BotFactory(channel, nickname)
        reactor.connectTCP(server, port, factory)
    reactor.run()

def main():
    import_plugins()
    run_server()

if __name__ == '__main__':
    main()

