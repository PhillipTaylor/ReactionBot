#!/usr/bin/env python
# -*- coding: utf-8



#from sqlalchemy import create_engine
#DATABASE_ENGINE = create_engine('sqlite:///:memory:')

DUMP_FILE = "irc_bot.data_dump.pickle"

# set all your connections here
CONNECTIONS = (
        #('irc.freenode.net', 6667, 'test_bot_1', 'twistedbot_1'),
        ('irc.freenode.net', 6667, 'test_bot_2', 'twistedbot_2'),
        )

# set plugins that should be loaded
PLUGINS = (
        #'plugins.reminder',
        #'plugins.feedreader',
        #'plugins.show_page_title',
        #'plugins.logger',
        #'plugins.nastywords',

        #'plugins.demo.periodic',
        #'plugins.demo.logger',
        #'plugins.demo.echo.handler',
        #'plugins.demo.userinfo',
        #'plugins.demo.custom_channels',
    )
