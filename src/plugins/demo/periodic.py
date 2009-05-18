#!/usr/bin/env python
# -*- coding: utf-8


import datetime

from core.plugins.manager import plugin_manager


class PeriodicAction(object):
    def __init__(self):
        self.last_call = datetime.datetime.now()

    def __call__(self):
        self.periodic_action()

    def periodic_action(self):
        now = datetime.datetime.now()
        message = "periodic in action: %s (last call: %s)" % \
                (now, self.last_call)
        for protocol in self.protocols:
            protocol.say(protocol.channel, message)
        self.last_call = now


class CustomChannelPeriodic(object):
    def __call__(self):
        for protocol in self.protocols:
            protocol.say(protocol.channel, "hello world!")


action = PeriodicAction()
custom_action = CustomChannelPeriodic()

# this will send message to all channels
plugin_manager.register_periodic(action, 20)
# this periodic will be visible only on choosen channels
plugin_manager.register_periodic(custom_action, 20, channels=['test_bot', ])
