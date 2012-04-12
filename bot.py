#!/usr/bin/env python
import configparser
import network
import linebuffer as lb
import quotestore
import re
from datetime import datetime
import logging
import sys

logging.basicConfig(filename='quotebot.log', level=logging.DEBUG)
nick = None
channels = None

#Find command regex
find_quote_single = re.compile('^!quotes? find [0-9]+$')
find_quote_range = re.compile('^!quotes? find [0-9]+ [0-9]+$')
find_quote_name = re.compile('^!quotes? find [A-Za-z_]+$')

#add command regex
add_quote_msg = re.compile('^!quote add [\w+\s?]+$')
add_quote_user = re.compile('^!quote add <[@+]?[A-Za-z_]+ [\w+\s?]+$')

events = {'PRIVMSG':'privmsg',
          '001':'welcome'}

def start():
  global nick
  global channels
  try:
    config_file = 'example.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)
    nick = config['settings']['nick']
    ident = config['settings']['ident']
    realname = config['settings']['realname']
    quote_file = config['settings']['quote file']
   
    host = config['server']['host']
    port = int(config['server']['port'])

    channels = config['server']['channels'].split(' ')
    logging.debug('Settings from file are nick = {0}, ident = {1}, realname = {2}, quote file = {3}'.format(nick, ident, realname, quote_file))
    
    logging.debug('Server settings are address = ({0}, {1}), channels = {2}'.format(host, port, channels))
    #set up quotestore with a given quote file
    #can be given max quotes parameter
    quotestore.initalise(quote_file)
    
    #set up the linebuffer
    lb.intialise()
  
    network.connect((host, port), nick, ident, host, realname)
 
  except KeyError as error:
    if error is 'Server':
     logging.error('[Server] section of config file is corrupt or missing')
     
    elif error is 'Settings':
      logging.error('[Settings] section of config file is corrupt or missing')
  
    else:
     logging.error('The value of {0} is missing or corrupt'.format(error))
    
    sys.exit(1)


def handle_messages(messages):
  for message in messages:
    handle_message(message)

def handle_message(message):
  global events
  prefix, command, params, endprefix = message
  if command in events:
    event = events[command]
    
    if event is 'welcome':
      on_welcome()
   
    elif event is 'privmsg':
      on_privmsg(params, endprefix, prefix)
    
    else:
      logging.debug('Unhandled command, {0}, occured'.format(event))

  else:
    logging.debug('Unknown event, {0}, occurred'.format(command))

def on_welcome():
  global channels
  network.join_all(channels)

def on_privmsg(params, message, source):
  global find_quote_single
  global find_quote_range
  global find_quote_name
  global add_quote_msg
  global add_quote_user
  channel = params[0]
  result = message.split(' ')
  answer = None

  if find_quote_single.match(message):
    print('find single')
    quote_id = int(result[2])
    answer = quotestore.get_quote(quote_id)

  elif find_quote_range.match(message):
    print('find range')
    start_id = int(result[2])
    end_id = int(result[3])
    answer = quotestore.get_quote_range(start_id, end_id)
  
  elif find_quote_name.match(message):
    print('find name')
    name = result[2]
    answer = quotestore.get_quotes_by_name(name)
  
  
  elif add_quote_msg.match(message):
    print('add quote message')
    parts = message.split(' ', 2)
    answer = lb.find_lines(channel, parts[2])
    if answer:
      answer = quotestore.add_quote(answer.line, answer.name, answer.time)
    
    else:
      answer = ['No matches found for that search']

  elif add_quote_user.match(message):
    print('add quote by user')
    parts = message.split(' ', 3)
    answer = lb.find_lines_by_name(channel, parts[2], parts[3])
    if answer:
      answer = quotestore.add_quote(answer.line, answer.name, answer.time)

    else:
      answer = ['No matches found for that search']

  elif message.startswith('!'):
    print('ignore malformed commands')

  else:
    now = datetime.today()
    timestamp = now.strftime('[%H:%M]')
    logging.debug(str.format('Adding line to linebuffer - ({0}, {1}, {2}, {3}', channel, message, source, timestamp))
    lb.add_line(channel, message, source, timestamp)
  
  print (answer)
  if answer:
    #if we have a response we send it
    network.msg(channel, answer)

  

start()
while True:
  messages = network.get_messages()
  handle_messages(messages)
