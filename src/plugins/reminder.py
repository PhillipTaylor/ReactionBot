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



MSG_COMMAND = getattr(settings, "REMINDER_COMMAND", ":msg ")
MSG_FORMAT = getattr(settings, "REMINDER_FORMAT",
            "%(to)s: [%(date)s] %(author)s powiedział: %(message)s")


class Reminder(object):

    implements(IStorable, IActionHandler)

    def __init__(self, name):
        self.mem = {}
        self.name = name

    def load(self, data):
        if data:
            self.mem = pickle.loads(data)

    def dump(self):
        return pickle.dumps(self.mem)

    def accepts_action(self, action):
        return action in ['privmsg', 'join']

    def handle_action(self, protocol, action, user, message):
        if action == 'privmsg':
            self.save_message(user, message)
        self.check_messages(protocol, user)

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
        author = user.split("!", 1)[0]
        if send_to == author:
            # do not save self sended messages
            return
        if not send_to in self.mem:
            self.mem[send_to] = []
        self.mem[send_to].append( {
                    "author": author,
                    "date": datetime.datetime.now(),
                    "to": send_to,
                    "message": message,
                })


reminder = Reminder(name='reminder')

plugin_manager.register(reminder)
