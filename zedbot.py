import config
import requests
import json
import socket
import re

def get_channel_id(channel):
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': config.client_id}

    url = f'https://api.twitch.tv/kraken/users?login={channel}'

    r = requests.get(url, headers=headers)

    data = json.loads(r.text)

    return data['users'][0]['_id']

def get_channel_followers(channel_id):
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': config.client_id}

    url = f'https://api.twitch.tv/kraken/channels/{channel_id}/follows'

    r = requests.get(url, headers=headers)

    return json.loads(r.text)

# Get channel id from channel name
channel_id = get_channel_id(config.channel)
# print(channel_id)

# Get list of followers from channel id
followers = get_channel_followers(channel_id)
# print(json.dumps(followers, indent=4))

# Should make a list comprehension for a list of follower ids

# Print channel followers in plaintext
# for user in followers['follows']:
#     print(user['user']['display_name'])

#############
# IRC STUFF #
#############
def send_nick(connection, nick):
    connection.send(f'NICK {nick}\r\n'.encode())

def send_pass(connection, password):
    connection.send(f'PASS {password}\r\n'.encode())

def join_channel(connection, channel):
    connection.send(f'JOIN {channel}\r\n'.encode())

def get_sender(msg):
    # Sender string (first item in list) looks like:
    # :user!user@user.tmi.twitch.tv
    result = ''
    for char in msg[0][1:]:
        if char == '!':
            return result
        result += char

def get_message(msg):
    result = ''
    for word in msg[3:]:
        result += word + ' '
    return result.lstrip(':').rstrip()

def send_message(connection, channel, msg):
    connection.send(f'PRIVMSG {channel} :{msg}\r\n'.encode())
    print(f'{config.username}: {msg}')

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
