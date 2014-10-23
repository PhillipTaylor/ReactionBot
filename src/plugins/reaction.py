# -*- coding: utf-8

import datetime
from random import choice

from zope.interface import implements

from core.plugins.interface import IActionHandler, IFinalize, IPeriodic
from core.plugins.manager import plugin_manager

SPEAK_INTERVAL = 3 * 60 # only speak every 3 minutes. make it more valuable!
RELOAD_INTERVAL = 15 * 60 # reload file every 15 minutes

class Reaction(object):
    implements(IActionHandler)

    # keyed on phrase, value is image.
    image_dictionary = {}
    last_message = None
    last_match = None

    def __init__(self, name, gifs_filename):
        self.name = 'plugin.' + name
        self.gifs_filename = gifs_filename
        self.last_reload = None

    def parse_file(self):

        if self.last_reload != None:

            diff = datetime.datetime.now() - self.last_reload
            if (diff.seconds < RELOAD_INTERVAL):
                return

        self.image_dictionary = {}
        logfile = open(self.gifs_filename, 'r')

        for line in logfile:
            line = line[:-1] # remove trailing new line
            if line not in (None, ''):
                parsed = line.split('=')
                if (len(parsed) > 1):
                    match_string = ' '.join(parsed[:-1]).strip()
                    urls = parsed[-1].strip()
                    self.image_dictionary[match_string] = urls.split(' ')

        logfile.close()
        self.last_reload = datetime.datetime.now()
        print "%d images available" % len(self.image_dictionary)

    def accepts_action(self, action):
        return action in ['privmsg', 'login', 'quit', 'exit']

    def handle_action(self, protocol, action, user, message):
        nick = user.split("!", 1)[0]

        self.parse_file()

        for key in self.image_dictionary.keys():
            if (message.lower().find(key.lower()) != -1):
                self.match_found(protocol, user, message, key)
                break

    def match_found(self, protocol, user, orig_message, match):

        if (orig_message.find("ReactionBot") == -1):
            # require a new word inorder to talk
            if self.last_match is not None:
                if self.last_match == match:
                    return

            # dont talk too often
            if self.last_message is not None:
                diff = datetime.datetime.now() - self.last_message
                if (diff.seconds < SPEAK_INTERVAL):
                    print "too early to reply"
                    return

        print "match: %s" % match
        urls = self.image_dictionary[match]

        # pick a url from the list at random
        url = choice(urls)

        ret_msg = "%s -> %s" % (match, url)
        print "[%s] message %s from %s triggered %s" % (
            datetime.datetime.now().strftime('%H:%M'),
            orig_message,
            user,
            ret_msg
        )

        protocol.say(protocol.channel, ret_msg)
        self.last_message = datetime.datetime.now()
        self.last_match = match

reaction = Reaction('reaction', 'data/reactions2.txt')
plugin_manager.register(reaction)
