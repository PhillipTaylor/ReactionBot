# -*- coding: utf-8

import datetime
from random import choice

from zope.interface import implements

from core.plugins.interface import IActionHandler, IFinalize, IPeriodic
from core.plugins.manager import plugin_manager

SPEAK_INTERVAL = 3 * 60 # only speak every 3 minutes. make it more valuable!

class Reaction(object):
    implements(IActionHandler)

    # keyed on phrase, value is image.
    image_dictionary = {}
    last_message = None
    last_match = None

    def __init__(self, name, gifs_filename):
        self.name = 'plugin.' + name
        
        logfile = open(gifs_filename, 'r')
        for line in logfile:
            line = line[:-1] # remove trailing new line
            if line not in (None, ''):
                parsed = line.split('=')
                if (len(parsed) > 1):
                    match_string = ' '.join(parsed[:-1]).strip()
                    urls = parsed[-1].strip()
                    self.image_dictionary[match_string] = urls.split(' ')

        logfile.close()

    def accepts_action(self, action):
        return action in ['privmsg', 'login', 'quit', 'exit']

    def handle_action(self, protocol, action, user, message):
        nick = user.split("!", 1)[0]

        for key in self.image_dictionary.keys():
            if (message.find(key) != -1):
                self.match_found(protocol, user, message, key)
                break

    def match_found(self, protocol, user, orig_message, match):

        # require a new word inorder to talk
        if user != "phill":
            if self.last_match is not None:
                if self.last_match == match:
                    return

            # dont talk too often
            if self.last_message is not None:
                diff = datetime.datetime.now() - self.last_message
                if (diff.seconds < SPEAK_INTERVAL):
                    print "too early to reply"
                    return

        urls = self.image_dictionary[match]

        # pick a url from the list at random
        url = choice(urls)

        ret_msg = "%s -> %s" % (match, url)
        print "message %s from %s triggered %s" % (
            orig_message,
            user,
            ret_msg
        )

        protocol.say(protocol.channel, ret_msg)
        self.last_message = datetime.datetime.now()
        self.last_match = match

reaction = Reaction('reaction', 'data/reactions.txt')
plugin_manager.register(reaction)
