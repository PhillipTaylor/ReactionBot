#!/usr/bin/env python
# -*- coding: utf-8


import datetime

from zope.interface import implements

from core.plugins.manager import plugin_manager
from core.plugins.interface import IPeriodic


class PeriodicAction(object):

    implements(IPeriodic)

    def __init__(self, sleep_time, max_calls):
        self.name = "periodic_%s" % datetime.datetime.now()
        self.call_counter = 0
        self.max_calls = max_calls
        self.sleep_time = sleep_time

    def periodic_handler(self, protocols):
        self.call_counter += 1
        for protocol in protocols:
            protocol.say(protocol.channel,
                    "periodic call nr: %d" % self.call_counter)
        if self.call_counter >= self.max_calls:
            self.loop.stop()



action = PeriodicAction(5, 3)
plugin_manager.register(action)
