import socket
import threading

import config
import irc
import twitch
import threads

# Get channel id from channel name
channel_id = twitch.get_channel_id(config.channel)

# Get initial list of follower ids from channel id
followers = twitch.get_follower_ids(channel_id)

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

print(f'Connected to {config.channel}\'s chat')

# Create and run thread to handle IRC communications
irc_manager = threads.IRCManager(c)
irc_thread = threading.Thread(target=irc_manager.run)
irc_thread.start()
