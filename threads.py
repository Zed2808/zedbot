import socket
import re
import time

import config
import irc
import twitch

class IRCManager():
    def __init__(self, connection):
        self.connection = connection

    def run(self):
        data = ''
        while True:
            try:
                # Get new data
                data = data + self.connection.recv(1024).decode()

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
                            irc.send_message(self.connection, channel, f'Hi {sender}! <3')

            except socket.error:
                print('> SOCKET ERROR')
            except socket.timeout:
                print('> SOCKET TIMEOUT')

class NewFollowerManager():
    def __init__(self, connection):
        self.connection = connection

    def run(self):
        # Get channel id from channel name
        self.channel_id = twitch.get_channel_id(config.channel)

        # Get initial list of follower ids from channel id
        self.followers = twitch.get_follower_ids(self.channel_id)

        while True:
            # Get current list of channel followers
            current_followers = twitch.get_follower_ids(self.channel_id)

            # Iterate through current followers
            for follower in current_followers:
                # If the current follower wasn't already in the list of followers from before
                if follower not in self.followers:
                    # Get follower's display name from their id
                    follower_name = twitch.get_username_by_id(follower)
                    print(f'> New follower: {follower_name}')

                    # Welcome new follower in chat
                    irc.send_message(self.connection, '#' + config.channel, f'Welcome {follower_name}!')

            # Save current followers to check against
            self.followers = current_followers

            time.sleep(5)
