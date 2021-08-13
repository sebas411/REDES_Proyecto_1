# REDES_Proyecto_1

## Description

This program was developed with the objective to learn about the xmpp protocol. It consists on a python file named client.py. This file is used as a command line interface and has a number of custom commands listed below. Using said commands you can connect to a xmpp server, login to your account and chat with other users.

## Getting Started

### Dependencies

* Python 3
* slixmpp module

### Installing

* First you need to clone or download the code of this repository to your computer.
* Then install the slixmpp module by running 'pip install slimxpp'

### Executing

* To execute the program run the command 'python3 client.py'

### Usage

#### Available commands

* quit  
  closes the program

* login [username] [password]  
  logs into xmpp account

* logout  
  logs you out of the account

* update  
  sends and receives notifications

* message [user] [message]  
  sends a message to specified user

* presence [status] [show]  
  sets custom status

* adduser [user]  
  adds a friend specified in [user]

* userdetails [user]  
  shows user details of specified user

* showusers  
  shows users and presence

* deleteaccount
  deletes the current account

* register [username] [password]  
  creates a user and logs into xmpp account

## Author

* Sebastián Maldonado 18003