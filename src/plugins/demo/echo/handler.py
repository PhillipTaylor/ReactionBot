#!/usr/bin/env python
# -*- coding: utf-8


from plugger import plugin_manager


def echo(protocol, user, channel, message, *params):
    nick = user.split("!", 1)[0]
    protocol.say(channel, "%s: %s" % (nick, message))

plugin_manager.register_action("privmsg", echo)
