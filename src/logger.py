# -*- coding: utf-8

import datetime

from zope.interface import implements

from core.plugins.interface import IActionHandler, IFinalize, IInitialize
from core.plugins.manager import plugin_manager



class Logger(object):
    implements(IActionHandler, IFinalize, IInitialize)

    def __init__(self, name, log_path):
        self.name = 'plugin.' + name
        self.log_path = log_path

    def finalize(self):
        if self.log_file:
            self.log_file.close()

    def initialize(self):
        self.log_file = open(self.log_path, 'wa')


    def accepts_action(self, action):
        return action == 'privmsg'

    def handle_action(self, protocol, action, user, message):
        nick = user.split("!", 1)[0]
        self.log_file.write("[%s] %s: %s" % \
                (datetime.datetime.now(), nick, message))


logger = Logger('logger', '/tmp/ircbot.log')
plugin_manager.register(logger)
