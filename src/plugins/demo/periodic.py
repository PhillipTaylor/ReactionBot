#!/usr/bin/env python
# -*- coding: utf-8


import datetime

from plugger import plugin_manager


class PeriodicAction(object):
    def __init__(self):
        self.last_call = datetime.datetime.now()

    def __call__(self):
        if self.manager.protocol:
            self.periodic_action()

    def periodic_action(self):
        now = datetime.datetime.now()
        message = "periodic in action: %s (last call: %s)" % \
                (now, self.last_call)
        self.manager.protocol.say(self.manager.protocol.channel, message)
        self.last_call = now


action = PeriodicAction()
plugin_manager.register_periodic(action, 15)
