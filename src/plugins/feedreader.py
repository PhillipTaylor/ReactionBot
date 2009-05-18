# -*- coding: utf-8


import time
import pickle
from datetime import datetime
import feedparser

from core.plugins.manager import plugin_manager


class FeedReader(object):
    """Feed objects manager"""

    def __init__(self, max_messages=6):
        self.feeds = {}
        self.feeds_battery = []
        self.max_messages = max_messages

    def set_feeds(self, feed_list):
        for (url, format) in feed_list:
            self.feeds[url] = {
                    'url' : url,
                    'format': format,
                    'last_update': datetime(2000, 1, 1),
                    }

    def fetch(self):
        for (id, feed) in self.feeds.iteritems():
            f = feedparser.parse(feed['url'])
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

    def __call__(self):
        self.periodic_action()

    def periodic_action(self):
        self.fetch()
        for i in self.feeds_battery[:self.max_messages]:
            feed = self.feeds_battery.pop(0)
            for protocol in self.protocols:
                protocol.say(protocol.channel, feed.encode('utf-8'))



feed_reader = FeedReader()
# set feeds that object should fetch
feed_reader.set_feeds([
        ('http://code.activestate.com/feeds/langs/python/',
                'ActiveState Code: %(title)s'),
    ])


# use plugin manager storage system
plugin_manager.register_storable(id='plugin.feedreader',
        loader=feed_reader.load, dumper=feed_reader.dump)
# this will send message to all channels
plugin_manager.register_periodic(feed_reader, 60 * 10,
        channels=['test_bot', ])
