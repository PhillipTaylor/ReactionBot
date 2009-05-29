#!/usr/bin/env python
# -*- coding: utf-8

import re

from zope.interface import implements
from twisted.web.client import getPage

from core.plugins.interface import IActionHandler
from core.plugins.manager import plugin_manager


class TitleFetcher(object):

    implements(IActionHandler)

    rx_url = re.compile(r'\b(http://\S+|www\.\S+)\b')
    rx_title = re.compile(r'<title>(.*?)</title>')

    name = 'plugin.title_fetcher'

    def accepts_action(self, action):
        return action == 'privmsg'

    def handle_action(self, protocol, action, user, message):
        "write a message to the file"
        for url in self.rx_url.findall(message):
            getPage(url).addCallback(self.send_page_title, protocol)

    def send_page_title(self, page, protocol):
        rx = self.rx_title.finditer(page)
        try:
            title = rx.next().groups()
            protocol.say(protocol.channel, 'title: "%s"' % title[0])
        except StopIteration:
            pass


plugin_manager.register(TitleFetcher())
