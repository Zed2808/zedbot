import socket
import re

import config
import irc
import twitch

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
                sender = irc.get_sender(line)
                message = irc.get_message(line)
                channel = line[2]

                print(f'{sender}: {message}')

                # Split message into list
                msg = message.split()

                # !hi
                if msg[0] == '!hi':
                    irc.send_message(c, channel, f'Hi {sender}! <3')

    except socket.error:
        print('SOCKET ERROR')
    except socket.timeout:
        print('SOCKET TIMEOUT')
