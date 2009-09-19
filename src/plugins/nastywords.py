#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re

from zope.interface import implements

from core.plugins.manager import plugin_manager
from core.plugins.interface import IStorable, IActionHandler

from twisted.python import log
import sys
log.startLogging(sys.stdout)


CMD_BAN = ':ban '
CMD_LIST = ':banlist '
CMD_UNBAN = ':unban '


class NastyRegexpFilter(object):

    implements(IStorable, IActionHandler)

    def __init__(self, name, admins):
        self.name = '%s.%s' % (type(self).__name__, name)
        self.admins = admins
        self._nasty_rx = []

    def dump(self):
        return pickle.dumps(self._nasty_rx)

    def load(self, data):
        self._nasty_rx = pickle.loads(data)

    def accepts_action(self, action):
        return action in ['privmsg', ]

    def handle_action(self, protocol, action, user, message):
        if message.startswith(CMD_BAN) and user in self.admins:
            # add new filter
            message = message[len(CMD_BAN):].split()
            rx = re.compile(message[0], re.IGNORECASE|re.UNICODE)
            reason = ' '.join(message[1:]) or None
            self._nasty_rx.append((rx, message[0], reason))
        elif message.startswith(CMD_LIST) and user in self.admins:
            # find matching filters and display them
            rx_filter = message[len(CMD_LIST):]
            for rx, rx_str, reason in self._nasty_rx:
                if rx_str.startswith(rx_filter):
                    response = 'rx: %s   reason: %s' % (rx_str, reason)
                    protocol.say(protocol.channel, response)
        elif message.startswith(CMD_UNBAN) and user in self.admins:
            # find matching filter and remove them
            rx_filter = message[len(CMD_UNBAN):]
            for i, (rx, rx_str, reason) in enumerate(self._nasty_rx):
                if rx_str == rx_filter:
                    self._nasty_rx.pop(i)
                    protocol.say(protocol.channel, 'unban: %s' % rx_str)
        else:
            # check if message contains banned word and kick user if does
            rx, reason = self.find_nasty_word(message)
            if rx:
                nick = user.split('!', 1)[0]
                protocol.kick(protocol.channel, nick, reason)

    def find_nasty_word(self, message):
        for rx, rx_str, reason in self._nasty_rx:
            if rx.search(message):
                return (rx, reason)
        return (None, None)


admins = set([
        'JohnDoe!i=john.doe@myname.com',
    ])
nasty_filter = NastyRegexpFilter('myfilter', admins)
plugin_manager.register(nasty_filter)
