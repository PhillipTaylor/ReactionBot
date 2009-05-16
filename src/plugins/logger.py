#!/usr/bin/env python
# -*- coding: utf-8


"""
Example plugin that logs all private messages
"""

import time

from plugger import plugg_manager


class MessageLogger:
    def __init__(self, path):
        self.file = open(path, "a")

    def log(self, user, channel, message, protocol):
        "write a message to the file"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


message_logger = MessageLogger("/tmp/twisted_bot.log")

plugg_manager.register("privmsg", message_logger.log)
