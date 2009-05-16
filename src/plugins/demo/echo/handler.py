#!/usr/bin/env python
# -*- coding: utf-8


from plugger import plugg_manager


def echo(user, channel, message, protocol):
    nick = user.split("!", 1)[0]
    protocol.say(channel, "%s: %s" % (nick, message))

plugg_manager.register("privmsg", echo)
