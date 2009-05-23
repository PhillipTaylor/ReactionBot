#!/usr/bin/env python
# -*- coding: utf-8


from zope.interface import Interface, Attribute


class IPlugin(Interface):
    """Base interface for all plugins and all plugin interfaces. Classes that do
    not implement ``IPlugin`` can not be used as plugin objects.
    """

    name = Attribute("Unique plugin object name")


class IStorable(IPlugin):
    """Interface for all plugins containing data that has to be stored and
    fetched when plugin is being loaded
    """

    def dump():
        """Returns string that will be stored"""

    def load(data):
        """Called with data - string returned by last `dump` call"""


class IInitialize(IPlugin):
    """Initialize plugin when loading"""

    def initialize():
        """Method called after loading the plugin"""


class IFinalize(IPlugin):
    """Finalize plugin when unloading"""

    def finalize():
        """Method called just before the plugin unload"""


class ICustomChannelsHandler(IPlugin):
    """Handle singals for choosen channnels"""

    def accepts_channel(channel):
        """Returns ``True`` if plugin is allowed to handle events for given
        channel. Returns ``False`` elsewhere.
        """


class IPeriodic(IPlugin):
    """Call periodic action handler"""

    sleep_time = Attribute("Time between calling `periodic_handler`")

    def periodic_handler(protocols):
        """Callback handler for periodic actions"""


class IActionHandler(IPlugin):
    """Handle choosen IRC message"""


    def accepts_action(action):
        """Returns ``True`` if plugins is allowed to handle given action,
        returns ``False`` elsewhere.
        """

    def handle_action(protocol, action, user, message):
        """Handle action"""


class ILineReceiver(IPlugin):
    """Plugin that handles all messages sended by server"""

    def handle_line(protocol, line):
        """Handle line reviced by given protocol instance"""

