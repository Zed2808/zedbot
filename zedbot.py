import socket
import threading

import config
import irc
import twitch
import threads

##############################################
# Set up IRC communications with Twitch chat #
##############################################

# IRC connection arguments
server = 'irc.twitch.tv'
nickname = config.username
channel = '#' + config.channel
port = 6667
password = config.oauth

# Create connection to server
c = socket.socket()
c.connect((server, port))

# Send server authentication and join channel
irc.send_pass(c, password)
irc.send_nick(c, nickname)
irc.join_channel(c, channel)

print(f'> Connected to {config.channel}\'s chat')

# Create and run thread to handle IRC communications
irc_manager = threads.IRCManager(c)
irc_thread = threading.Thread(target=irc_manager.run)
irc_thread.start()

print('> Started IRC thread...')

#############################
# Set up Twitch API threads #
#############################

# Create and run new follower alert thread
new_follower_manager = threads.NewFollowerManager(c)
new_follower_thread = threading.Thread(target=new_follower_manager.run)
new_follower_thread.start()

print('> Started new follower thread...')
