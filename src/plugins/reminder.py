#!/usr/bin/env python
# -*- coding: utf-8


"""
send message to absent users

Usage:

    :msg <User nick> <message>
"""

import datetime
import pickle

from zope.interface import implements

import settings
from core.plugins.manager import plugin_manager
from core.plugins.interface import IStorable, IActionHandler
from core.plugins.interface import ICustomChannelsHandler



MSG_COMMAND = getattr(settings, "REMINDER_COMMAND", ":msg ")
MSG_FORMAT = getattr(settings, "REMINDER_FORMAT",
            "%(author)s: [%(date)s] %(to)s powiedział: %(message)s")


class Reminder(object):

    implements(IStorable, IActionHandler, ICustomChannelsHandler)

    def __init__(self, name, channels):
        self.mem = {}
        self.name = name
        self.channels = channels

    def load(self, data):
        if data:
            self.mem = pickle.loads(data)

    def dump(self):
        return pickle.dumps(self.mem)

    def accepts_channel(self, channel):
        return channel in self.channels

    def accepts_action(self, action):
        return action in ['privmsg', 'join']


    def handle_action(self, protocol, action, user, message):
        self.check_messages(protocol, user)
        if action == 'privmsg':
            self.save_message(user, message)

    def check_messages(self, protocol, user):
        nick = user.split("!", 1)[0]
        if nick in self.mem:
            protocol.say(protocol.channel,
                    " # ".join((MSG_FORMAT % m for m in self.mem[nick])))
            del self.mem[nick]

    def save_message(self, user, message):
        if not message.startswith(MSG_COMMAND):
            return
        message = message[len(MSG_COMMAND):].strip()
        send_to, message = message.split(' ', 1)
        if not send_to in self.mem:
            self.mem[send_to] = []
        self.mem[send_to].append( {
                    "author": user.split("!", 1)[0],
                    "date": datetime.datetime.now(),
                    "to": send_to,
                    "message": message,
                })


reminder_1 = Reminder(name='reminder.first', channels=['test_bot', ])
reminder_2 = Reminder(name='reminder.second',
        channels=['test_bot_2', 'test_bot_3'])

plugin_manager.register(reminder_1)
plugin_manager.register(reminder_2)
