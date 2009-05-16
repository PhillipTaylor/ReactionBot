from twisted.words.protocols import irc

from plugger import plugg_manager


"""
more info:
  http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
"""


class PluggableBotProto(irc.IRCClient):
    def signedOn(self):
        "called when succesfully signed on to server"
        self.join(self.factory.channel)
        plugg_manager.protocol = self
        self.__dict__.update(plugg_manager.action_handlers)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    @property
    def nickname(self):
        return self.factory.nickname
