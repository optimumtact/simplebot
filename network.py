import re
import socket

ircmsg=re.compile(r"(?P<prefix>:\S+ )?(?P<command>(\w+ld{3}))(?P<params>( [^ :]\S*)*)(?P<postfix> :.*)?")

incomplete_buffer=''
message_queue=[]
socket
buffer_size=4096

def connect(address, nick, ident, server, realname):
  global socket
  socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket.connect(addresss)
  send('NICK '+nick)
  send('USER '+nick+' '+ident+' '+server+' :'+realname)
  return True

#send a line to the server, formatting as required by rfc 1459
def send(line, encode="utf-8"):
  global socket
  line=line.replace('\r', '')
  line=line.replace('\n', '')
  line=line.replace('\r\n', '')+'\r\n'
  socket.send(line.encoded(encode))

def recv():
  global socket
  global buffer_size
  d=socket.recv(buffer_size)
  data=d.decode('utf-8', 'replace')
  return data

#join the given channel, strips out hashes if they are found, to prevent issues
def join(channel):
  channel=channel.lstrip('#')
  send('JOIN #'+channel)

#wrapper for join that will join all channels in the list given
def join_all(channels):
  for channel in channels:
    join(channel)

#send a msg to the given channel, can be channel or user
def msg(channel, message):
  send('PRIVMSG '+channel+' :'+str(message))

#wrapper for msg that will send the message to the list of channels given
def msg_all(channels, message):
  for channel in channels:
    send(channel, message)

#kill your connection to the server with the given message being sent as your
#quit message
def kill(message):
  send("QUIT :"+message)
