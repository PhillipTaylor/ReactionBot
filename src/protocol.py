from twisted.words.protocols import irc

from plugger import plugin_manager


"""
more info:
  http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
"""


class PluggableBotProto(irc.IRCClient):
    def __init__(self):
        plugin_manager.protocol = self
        self.__dict__.update(plugin_manager.action_handlers)

    def signedOn(self):
        "called when succesfully signed on to server"
        self.join(self.factory.channel)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    @property
    def nickname(self):
        return self.factory.nickname

    @property
    def channel(self):
        return self.factory.channel
