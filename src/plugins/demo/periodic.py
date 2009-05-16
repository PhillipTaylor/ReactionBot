#!/usr/bin/env python
# -*- coding: utf-8


import datetime

from twisted.internet import task



class PeriodicAction(object):
    def __init__(self):
        self.last_call = None

    def __call__(self):
        now = datetime.datetime.now()
        print "current time: %s (last call: %s)" % (now, self.last_call)
        self.last_call = now


periodic = PeriodicAction()
t = task.LoopingCall(periodic)
t.start(5)
