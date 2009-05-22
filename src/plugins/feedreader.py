# -*- coding: utf-8


import time
import pickle
from datetime import datetime
import feedparser

from zope.interface import implements
from twisted.web.client import getPage

from core.plugins.manager import plugin_manager
from core.plugins.interface import IPeriodic, IStorable

class FeedReader(object):
    """Feed objects manager"""

    implements(IPeriodic, IStorable)

    def __init__(self, name, sleep_time, max_messages=6):
        self.feeds = {}
        self.feeds_battery = []
        self.max_messages = max_messages
        self.name = "periodic." + name
        self.sleep_time = sleep_time

    def set_feeds(self, feed_list):
        for (url, format) in feed_list:
            self.feeds[url] = {
                    'url' : url,
                    'format': format,
                    'last_update': datetime(2000, 1, 1),
                    }

    def fetch(self):
        for (id, feed) in self.feeds.iteritems():
            # because it is all twisted powered, use twisted to fetch each rss
            deferred = getPage(feed['url'])
            deferred.addCallback(self._feed_callback, feed)

    def _feed_callback(self, feed_page, feed):
        f = feedparser.parse(feed_page)
        for entry in f['entries']:
            update = entry['updated_parsed']
            if datetime.fromtimestamp(time.mktime(update)) > feed['last_update']:
                self.feeds_battery.append(feed['format'] % entry)
        feed['last_update'] = datetime.now()


    def load(self, data):
        if not data:
            return
        loaded = pickle.loads(data)
        self.feeds_battery = loaded['feeds_battery']
        feed_list = loaded['feeds_list']
        for feed in feed_list:
            if feed in self.feeds:
                self.feeds[feed]['last_update'] = feed_list[feed]['last_update']
            else:
                self.feeds[feed] = feed_list[feed]

    def dump(self):
        return pickle.dumps({
                'feeds_list': self.feeds,
                'feeds_battery': self.feeds_battery
            })

    def periodic_handler(self, protocols):
        self.fetch()
        for i in self.feeds_battery[:self.max_messages]:
            feed = self.feeds_battery.pop(0)
            for protocol in protocols.filter(channels=['test_bot', ]):
                protocol.say(protocol.channel, feed.encode('utf-8'))



feed_reader = FeedReader("pyrss", 60 * 15)
# set feeds that object should fetch
feed_reader.set_feeds([
        ('http://code.activestate.com/feeds/langs/python/',
                'ActiveState Code: %(title)s'),
    ])

plugin_manager.register(feed_reader)
