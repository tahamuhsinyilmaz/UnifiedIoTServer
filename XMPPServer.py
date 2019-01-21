import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from database import database
import datetime

class Server(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')


    def session_start(self, event):
        self.send_presence()
        try:
            self.get_roster()
        except IqError as err:
            logging.error('There was an error getting the roster')
            logging.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            logging.error('Server is taking too long to respond')
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
            self.parseMessage(msg)

    def parseMessage(self,msg):
        # print("Message is {0} arrived from {1}".format(msg.__getitem__('body'),msg.__getitem__('from')))
        # print("xmpp "+msg.__getitem__('body'))
        database().insert_value('XMPP', datetime.datetime.now(), str(msg.__getitem__('body')))


def main():
    jid="innerclient@localhost"
    password="Taha2010"
    xmpp = Server(jid, password)
    if xmpp.connect():
        xmpp.process(block=True)