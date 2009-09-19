Creating new plugin 
===================

So you want to write your own plugin? 


Echo plugin
-----------

Each plugin has to implement at least :class:`interface.IPlugin` interface.
Because echo should work only for user *privmsg* message, we need to use
:class:`interface.IActionHandler` which allready inherits from
:class:`interface.IPlugin`::

    from zope.interface import implements
    
    from core.plugins.interface import IActionHandler
    from core.plugins.manager import plugin_manager


    class Echo(object):

        implements(IActionHandler)

        def __init__(self, name):
            self.name = '%s.%s' % (type(self).__name__, name)

        def accepts_action(self, action):
            return action in ['privmsg', ]

        def handle_action(self, protocol, action, user, message):
            response = 'echo: %s' % message
            protocol.say(protocol.channel, response)

    echo = Echo('my_echo')
    plugin_manager.register(echo)


Done, echo plugin is ready. I've wrote class that implements all
:class:`interface.IPlugin` and :class:`interface.IActionHandler` attributes.
Then I've created instance of that class and registered to let txIRCbot know
about it. But there's one more thing that needs to be done. In *settings.py*
file add path to that module, written in dot notation. For example, if it's
*plugins/myplugin/echo.py*, `settings.PLUGINS` tuple will contain
`"plugins.myplugin.echo"` string.

txIRCbot may join more than one server and channel. If so, we may want some
plugin instances works only for custom channels. How to do this? It's simple
-- just implement :class:`interface.ICustomChannelsHandler` interface::

    from core.plugins.interface import ICustomChannelsHandler

    class Echo(object):

        implements(IActionHandler, ICustomChannelsHandler)

        def accepts_channel(self, channel):
            return channel in ['python', 'mychan']

        # ...

Now, how about doing random *echo* every 5 minutes?::

    import random

    from core.plugins.interface import IPeriodic

    class Echo(object):

        implements(IActionHandler, ICustomChannelsHandler, IPeriodic)

        def __init__(self, name):
            self.name = '%s.%s' % (type(self).__name__, name)
            self.sleep_time = 60 * 5
            self._echo_msg = []

        def handle_action(self, protocol, action, user, message):
            response = 'echo: %s' % message
            # remember response
            self._echo_msg.append(response)
            protocol.say(protocol.channel, response)

        def periodic_handler(self, protocols):
            message = random.choice(self._echo_msg)
            for protocol in protocols:
                protocol.say(protocol.channel, message)
            # clean responses list
            self._echo_msg = []

        # ...

So far so good, but what if we need to close the application 4 minutes after
last random echo call? If we don't want to loose `_echo_msg` list, we need to
write is somewhere. That's what :class:`interface.IStorable` is doing::


    import pickle

    from core.plugins.interface import IStorable

    class Echo(object):

        implements(IActionHandler, ICustomChannelsHandler, 
                IPeriodic, IStorable)
    
        def dump(self):
            return pickle.dumps(self._echo_msg)

        def load(self, data):
            if data:
                self._echo_msg.extend(pickle.loads(data))

        # ...

