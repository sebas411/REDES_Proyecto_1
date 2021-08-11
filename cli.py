#!/usr/bin/python
import sys, os, xmpp

connected = False

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
            jid = xmpp.protocol.JID(user)
            cl = xmpp.Client(jid.getDomain(), debug=[])
            cl.connect()
            cl.auth(jid.getNode(), psw)
            cl.send(xmpp.protocol.Message('sebas1@alumchat.xyz', "funciona"))
    else:
        print("Command not found")