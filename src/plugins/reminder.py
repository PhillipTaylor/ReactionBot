#!/usr/bin/env python
# -*- coding: utf-8


"""
send message to absent users

Usage:

    :msg <User nick> <message>
"""

import datetime
import pickle

import settings
from core.plugins.manager import plugin_manager


MSG_COMMAND = getattr(settings, "REMINDER_COMMAND", ":msg ")
MSG_FORMAT = getattr(settings, "REMINDER_FORMAT",
            "%(author)s: [%(date)s] %(to)s powiedział: %(message)s")


class Reminder(object):
    def __init__(self):
        self.mem = {}

    def loads(self, data):
        self.mem = pickle.loads(data)

    def dumps(self):
        return pickle.dumps(self.mem)

    def on_user_joined(self, user, channel, protocol):
        self.check_messages(user, channel, protocol)

    def on_privmsg(self, user, channel, message, protocol):
        self.check_messages(user, channel, protocol)
        try:
            self.save_message(user, message)
        except ValueError:
            pass

    def check_messages(self, user, channel, protocol):
        nick = user.split("!", 1)[0]
        if nick in self.mem:
            protocol.say(channel,
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


reminder = Reminder()

# use plugin manager storage system
plugin_manager.register_storable(id='plugin.reminder',
        loader=reminder.loads, dumper=reminder.dumps)

# register chooser action handlers
plugin_manager.register_action('userJoined', reminder.on_user_joined)
plugin_manager.register_action('privmsg', reminder.on_privmsg)
