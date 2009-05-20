#!/usr/bin/env python
# -*- coding: utf-8


from zope.interface import implements

from core.plugins.interface import IActionHandler
from core.plugins.manager import plugin_manager

class Echo(object):

    implements(IActionHandler)

    name = 'echo'

    def accepts_action(self, action):
        return action in ['privmsg', ]

    def handle_action(self, protocol, action, user, message):
        nick = user.split("!", 1)[0]
        protocol.say(protocol.channel, "%s: %s" % (nick, message))


echo = Echo()
plugin_manager.register(echo)
