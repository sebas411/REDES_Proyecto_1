import asyncio

from slixmpp import ClientXMPP
from slixmpp.exceptions import IqTimeout, IqError


class Client(ClientXMPP):

  def __init__(self, jid, password):
    ClientXMPP.__init__(self, jid, password)
    self.id = jid
    self.psw = password

    self.add_event_handler("message", self.message)
    self.add_event_handler("session_start", self.session_start)
    self.add_event_handler("register", self.registerusr)

    self.register_plugin('xep_0030') 
    self.register_plugin('xep_0004')
    self.register_plugin('xep_0077')
    self.register_plugin('xep_0199')
    self.register_plugin('xep_0066')

  async def registerusr(self, iq):
    siq = self.Iq()
    siq['register']['username'] = self.id.split('@')[0]
    siq['register']['password'] = self.psw
    siq['type'] = "set"
    try: await siq.send()
    except: pass

  #all logic goes here
  async def session_start(self, event):
    self.send_presence()
    await self.get_roster()
    while True:
      commandline = input("xmppCli (%s)> "%self.id).split(' ')
      command = commandline[0]
      args = commandline[1:]

      if command == "quit":
        print("Please logout first")
        await self.get_roster()

      elif command == "logout":
        self.disconnect()
        await self.get_roster()

      elif command == "login": print("You are already logged in")

      elif command == "register": print("You are already logged in")

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
          print()
          user = args[0]
          cn = self.client_roster.presence(user)
          if len(cn) == 0: print("user %s is away"%user)
          else:
            for connection in cn:
              default = 'available'
              if cn[connection]['show']:
                print("user %s is"%user, cn[connection]['show'],',',cn[connection]['status'])
              else:
                print("user %sis"%user, default,',',cn[connection]['status'])
          print()
        else: print("incorrect amount of arguments")
      
      elif command == "showusers":
        contacts = self.client_roster.groups()
        for contact in contacts:
          print()
          for user in contacts[contact]:
            if user == self.id: continue
            cn = self.client_roster.presence(user)
            if len(cn) == 0: print("user %s is away"%user)
            else:
              for connection in cn:
                default = 'available'
                if cn[connection]['show']:
                  print("user %s is"%user, cn[connection]['show'],',',cn[connection]['status'])
                else:
                  print("user %s is"%user, default,',',cn[connection]['status'])
          print()

      elif command == "deleteaccount":
        iq = self.Iq()
        #set remove
        iq['register']['remove'] = True
        iq['type'] = "set"
        iq['from'] = self.id
        iq.send()
        #close connection
        self.disconnect()
        await self.get_roster()

      else:
        print("command not found")

      await self.get_roster()

  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      print("%(from)s says: %(body)s"% msg)

async def session(user, psw):
  pass


if __name__ == '__main__':

  while True:
    commandline = input("xmppCli> ").split(' ')
    command = commandline[0]
    args = commandline[1:]
    if command == "quit":
      break
    elif command == "login":
      if len(args) >= 2:
        user = args[0]
        psw = args[1]
        xmpp = Client(user, psw)
        xmpp.connect()
        xmpp.process(forever=False)
        connected = True
      else:
        print("command missing arguments")
    elif command == "register":
      if len(args) >= 2:
        user = args[0]
        psw = args[1]
        xmpp = Client(user, psw)
        #registrar
        xmpp["xep_0077"].force_registration = True

        xmpp.connect()
        xmpp.process(forever=False)
        connected = True
      else:
        print("command missing arguments")
    else:
      print("command not found or not logged in")

      

  