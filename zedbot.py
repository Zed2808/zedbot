import socket
import re

import config
from irc import *
from twitch_api import *

# Get channel id from channel name
channel_id = get_channel_id(config.channel)

# Get list of follower ids from channel id
followers = get_follower_ids(channel_id)

# Print channel followers in plaintext
# for user in followers['follows']:
#     print(user['user']['display_name'])

#############
# IRC STUFF #
#############
server = 'irc.twitch.tv'
nickname = config.username
channel = '#' + config.channel
port = 6667
password = config.oauth

# Create connection to server
c = socket.socket()
c.connect((server, port))

send_pass(c, password)
send_nick(c, nickname)
join_channel(c, channel)

print(f'Connected to {config.channel}\'s chat')

data = ''

while True:
    try:
        # Get new data
        data = data + c.recv(1024).decode()

        # Split data to get only new data
        data_split = re.split(r'[\r\n]+', data)
        data = data_split.pop()

        # For each line in the new data
        for line in data_split:
            # Split line
            line = line.split()

            # If data is a regular chat message
            if line[1] == 'PRIVMSG':
                # Get message details
                sender = get_sender(line)
                message = get_message(line)
                channel = line[2]

                print(f'{sender}: {message}')

                # Split message into list
                msg = message.split()

                # !hi
                if msg[0] == '!hi':
                    send_message(c, channel, f'Hi {sender}! <3')

    except socket.error:
        print('SOCKET ERROR')
    except socket.timeout:
        print('SOCKET TIMEOUT')
