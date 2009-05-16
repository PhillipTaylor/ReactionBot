#!/usr/bin/env python
# -*- coding: utf-8


"""
send message to absent users

Usage:

    :msg <User nick> <message>
"""

import datetime

import settings
import memorycache
from plugger import plugin_manager

if not hasattr(settings, "REMINDER_COMMAND"):
    setattr(settings, "REMINDER_COMMAND", ":msg ")
if not hasattr(settings, "REMINDER_FORMAT"):
    setattr(settings, "REMINDER_FORMAT",
            "%(author)s: [%(date)s] %(to)s powiedział: %(message)s")


cache = memorycache.MemoryCache()
if hasattr(settings, 'DATABASE_ENGINE'):
    try:
        import dbcache
        cache = dbcache.DbCache()
    except ImportError:
        pass



class Reminder(object):
    def __init__(self):
        self.cache = cache

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
        messages = self.cache.get(nick)
        if messages:
            for message in messages:
                protocol.say(channel, message)
            self.cache.drop(user)

    def save_message(self, user, message):
        if not message.startswith(settings.REMINDER_COMMAND):
            return
        send_to, message = message[len(settings.REMINDER_COMMAND):].split(' ', 1)
        log = settings.REMINDER_FORMAT % {
                    "author": user.split("!", 1)[0],
                    "date": datetime.datetime.now(),
                    "to": send_to,
                    "message": message,
                }
        cache.add(send_to, log)


reminder = Reminder()
plugin_manager.register_action('userJoined', reminder.on_user_joined)
plugin_manager.register_action('privmsg', reminder.on_privmsg)
