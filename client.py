import asyncio

from slixmpp import ClientXMPP


class Client(ClientXMPP):

  def __init__(self, jid, password):
    ClientXMPP.__init__(self, jid, password)
    self.id = jid

    self.add_event_handler("message", self.message)
    self.add_event_handler("session_start", self.session_start)


  #all logic goes here
  async def session_start(self, event):
    self.send_presence()
    await self.get_roster()
    while True:
      commandline = input("xmppCli (%s)> "%self.id).split(' ')
      command = commandline[0]
      args = commandline[1:]

      if command == "quit":
        print("Please loggout first")
        await self.get_roster()

      elif command == "loggout":
        self.disconnect()

      elif command == "login": print("You are already logged in")

      elif command == "message":
        if len(args) >= 2:
          to = args[0]
          msg = ' '.join(args[1:])
          self.send_message(to, msg, mtype='chat')
        else:
          print("command missing arguments")

      elif command == "update": await self.get_roster()

      elif command == "presence":
        if len(args) >= 2:
          status = args[0]
          show = args[1]
          self.send_presence(show, status)
        else:
          print("command missing arguments")

      elif command == "adduser":
        if len(args) == 1:
          user = args[0]
          self.send_presence_subscription(user)
        else: print("incorrect amount of arguments")
      
      elif command == "userdetails":
        if len(args) == 1:
          user = args[0]
          user = self.client_roster.presence(user)
          for pres in user.items():
            print("%(show)s %(status)s"%(pres, pres))
        else: print("incorrect amount of arguments")
      
      elif command == "showusers":
        contacts = self.client_roster.groups()
        for contact in contacts:
          print(contact)

      else:
        print("command not found")

      await self.get_roster()

  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      print("%(from)s says: %(body)s"% msg)

async def session(user, psw):
  pass


if __name__ == '__main__':
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
        if len(args) >= 2:
          user = args[0]
          psw = args[1]
          xmpp = Client(user, psw)
          xmpp.connect()
          xmpp.process(forever=False)
          connected = True
        else:
          print("command missing arguments")
    else:
      print("command not found or not logged in")

      

  