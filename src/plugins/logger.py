# -*- coding: utf-8

import datetime

from zope.interface import implements

from core.plugins.interface import IActionHandler, IFinalize, IPeriodic
from core.plugins.manager import plugin_manager



class Logger(object):
    implements(IActionHandler, IFinalize, IPeriodic)

    def __init__(self, name, log_path):
        self.name = 'plugin.' + name
        self.log_path = log_path
        self.log_file = open(self.log_path, 'a')

    def finalize(self):
        if self.log_file:
            self.log_file.close()

    def accepts_action(self, action):
        return action in ['privmsg', 'login', 'quit', 'exit']

    def handle_action(self, protocol, action, user, message):
        nick = user.split("!", 1)[0]
        self.log_file.write("[%s] %s: %s\n" % \
                (datetime.datetime.now(), nick, message))

    sleep_time = 60

    def periodic_handler(self, protocols):
        self.log_file.flush()



logger = Logger('logger', '/tmp/ircbot.log')
plugin_manager.register(logger)
