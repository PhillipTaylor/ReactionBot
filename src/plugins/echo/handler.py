#!/usr/bin/env python
# -*- coding: utf-8


from plugger import plugg_manager


def echo(user, channel, message, protocol):
    print "echo", protocol
    protocol.say(channel, "echo: %s" % message)

plugg_manager.register("privmsg", echo)
