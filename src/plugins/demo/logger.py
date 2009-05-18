#!/usr/bin/env python
# -*- coding: utf-8


"""
Example plugin that logs all private messages
"""

import time

from core.plugins.manager import plugin_manager


class MessageLogger:
    def __init__(self, path):
        self.file = open(path, "a")

    def log(self, protocol, user, channel, message, *params):
        "write a message to the file"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        nick = user.split("!", 1)[0]
        self.file.write('(#%s) %s %s: %s\n' % \
                (protocol.channel, timestamp, nick, message))
        self.file.flush()

    def close(self):
        self.file.close()


message_logger = MessageLogger("/tmp/twisted_bot.log")

plugin_manager.register_action("privmsg", message_logger.log)
