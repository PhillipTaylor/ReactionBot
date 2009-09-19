#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re

from zope.interface import implements

from core.plugins.manager import plugin_manager
from core.plugins.interface import IStorable, IActionHandler


CMD_BAN = ':ban'

class NastyRegexpFilter(object):

    implements(IStorable, IActionHandler)

    def __init__(self, name):
        self.name = '%s.%s' % (type(self).__name__, name)
        self._nasty_rx = []

    def dump(self):
        return pickle.dumps(self._nasty_rx)

    def load(self, data):
        self._nasty_rx = pickle.loads(data)

    def accepts_action(self, action):
        return action in ['privmsg', ]

    def handle_action(self, protocol, action, user, message):
        if message.startswith(CMD_BAN):
            message = message.split()
            rx = re.compile(message[1], re.IGNORECASE|re.UNICODE)
            reason = ' '.join(message[2:]) or None
            self._nasty_rx.append((rx, reason))
            response = 'nasty word: %s  reason: %s' % (message[1], reason)
            protocol.say(protocol.channel, response)
        else:
            rx, reason = self.find_nasty_word(message)
            if rx:
                nick = user.split('!', 1)[0]
                protocol.kick(protocol.channel, nick, reason)

    def find_nasty_word(self, message):
        for rx, reason in self._nasty_rx:
            if rx.search(message):
                return (rx, reason)
        return (None, None)


nasty_filter = NastyRegexpFilter('myfilter')
plugin_manager.register(nasty_filter)
