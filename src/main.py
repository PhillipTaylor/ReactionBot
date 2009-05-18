#!/usr/bin/env python
# -*- coding: utf-8

from optparse import OptionParser

from twisted.internet import reactor

from factory import BotFactory
from core.plugins.manager import plugin_manager
import settings


def import_plugins():
    for plug in settings.PLUGINS:
        __import__(plug)

def run_server():
    for (server, port, channel, nickname) in settings.CONNECTIONS:
        factory = BotFactory(channel, nickname)
        reactor.connectTCP(server, port, factory)
    reactor.callLater(5, plugin_manager.start_periodics)
    reactor.run()

def main():
    parser = OptionParser()
    parser.add_option("-t", "--test-plugins", dest="test_plugins",
            action="store_true", help="load plugins and quit", default=False)
    parser.add_option("-p", "--plain", dest="plain", action="store_true",
            help="run bot without loading plugins", default=False)
    (options, args) = parser.parse_args()

    try:
        if not options.plain:
            import_plugins()
        plugin_manager.plugins_initialize()
        if not options.test_plugins:
            run_server()
    finally:
        plugin_manager.plugins_finalize()


if __name__ == '__main__':
    main()
