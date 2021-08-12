import asyncio
import logging

from slixmpp import ClientXMPP


class Client(ClientXMPP):

  def __init__(self, jid, password):
    ClientXMPP.__init__(self, jid, password)

    self.add_event_handler("message", self.message)
    self.add_event_handler("session_start", self.session_start)

    # If you wanted more functionality, here's how to register plugins:
    # self.register_plugin('xep_0030') # Service Discovery
    # self.register_plugin('xep_0199') # XMPP Ping

    # Here's how to access plugins once you've registered them:
    # self['xep_0030'].add_feature('echo_demo')

  async def session_start(self, event):
    self.send_presence()
    self.get_roster()
    while True:
      commandline = input("xmppCli> ").split(' ')
      command = commandline[0]
      args = commandline[1:]
      if command == "quit":
        break
      elif command == "login":
        print("You are already logged in")
      elif command == "message":
        if len(args) < 2: continue
        to = args[0]
        msg = args[1]
        self.send_message(to, msg, mtype='chat')

    # Most get_*/set_* methods from plugins use Iq stanzas, which
    # are sent asynchronously. You can almost always provide a
    # callback that will be executed when the reply is received.

  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      print("Message: %(body)s"% msg)
      #msg.reply("Thanks for sending\n%(body)s" % msg).send()

async def session(user, psw):
  pass


if __name__ == '__main__':
  # Ideally use optparse or argparse to get JID,
  # password, and log level.

  #logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

  connected = False
  xmpp = 0

  while True:
    commandline = input("xmppCli> ").split(' ')
    command = commandline[0]
    args = commandline[1:]
    if command == "quit":
      break
    elif command == "login":
      if connected: print("You are already logged in")
      else:
        user = args[0]
        psw = args[1]
        xmpp = Client('echobot@alumchat.xyz', 'boty')
        xmpp.connect()
        xmpp.process(forever=False)
        connected = True
    elif command == "message":
      if len(args) < 2: continue
      to = args[0]
      msg = args[1]
      if connected:
        xmpp.send_message(to, msg, mtype='chat')

    print(command, args)
      

  