#!/usr/bin/env python
# -*- coding: utf-8



#from sqlalchemy import create_engine
#DATABASE_ENGINE = create_engine('sqlite:///:memory:')

DUMP_FILE = "irc_bot.data_dump.pickle"

# set all your connections here
CONNECTIONS = (
        #('irc.freenode.net', 6667, 'test_bot_1', 'twistedbot_1'),
        ('grunt.net-a-porter.com', 6667, 'merch', 'Reaction Bot!Reaction Bot'),
        ('grunt.net-a-porter.com', 6667, 'idlechat', 'Reaction Bot!Reaction Bot'),
       # ('grunt.net-a-porter.com', 6667, 'reactionbot', 'Reaction Bot!Reaction Bot'),
        )

# set plugins that should be loaded
PLUGINS = (
        #'plugins.reminder',
        #'plugins.feedreader',
        #'plugins.show_page_title',
        #'plugins.logger',
        #'plugins.nastywords',
        'plugins.reaction',

        #'plugins.demo.periodic',
        #'plugins.demo.logger',
        #'plugins.demo.echo.handler',
        #'plugins.demo.userinfo',
        #'plugins.demo.custom_channels',
    )
