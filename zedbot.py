import socket
import threading

import config
import irc
import twitch
import threads

# Get Twitch channel id
channel_id = twitch.get_channel_id(config.channel)

##############################################
# Set up IRC communications with Twitch chat #
##############################################

# IRC connection arguments
server = 'irc.twitch.tv'
nickname = config.username
channel = '#' + config.channel
port = 6667
password = 'oauth:' + config.oauth

# Create connection to server
c = socket.socket()
c.connect((server, port))

# Send server authentication and join channel
irc.send_pass(c, password)
irc.send_nick(c, nickname)
irc.join_channel(c, channel)

print(f'> Connected to {config.channel}\'s chat')

# Create and run thread to handle IRC communications
irc_manager = threads.IRCManager(channel_id, c)
irc_thread = threading.Thread(target=irc_manager.run)
irc_thread.start()

print('> Started IRC thread...')

#############################
# Set up Twitch API threads #
#############################

# Create and run new follower alert thread
new_follower_manager = threads.NewFollowerManager(channel_id, c)
new_follower_thread = threading.Thread(target=new_follower_manager.run)
new_follower_thread.start()

print('> Started new follower thread...')
