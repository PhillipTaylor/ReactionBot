#!/usr/bin/env python
# -*- coding: utf-8


"""
Example plugin that logs all private messages
"""


import time

from zope.interface import implements

from core.plugins.interface import IActionHandler, IInitialize, IFinalize
from core.plugins.manager import plugin_manager



class MessageLogger(object):

    implements(IActionHandler, IInitialize, IFinalize)

    def __init__(self, path):
        self.log_path = path
        self.name = "message_logger"

    def initialize(self):
        self.file = open(self.log_path, "a")

    def finalize(self):
        self.file.close()

    def accepts_action(self, action):
        return action in ['privmsg', 'ping', 'join']

    def handle_action(self, protocol, action, user, message):
        "write a message to the file"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        nick = user.split("!", 1)[0]
        self.file.write('(#%s) %s %s: %s\n' % \
                (protocol.channel, timestamp, nick, message))
        self.file.flush()


logger = MessageLogger("/tmp/message_logger.log")
plugin_manager.register(logger)
