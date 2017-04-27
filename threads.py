import socket
import re
import time

import config
import irc
import twitch

class IRCManager():
    def __init__(self, channel_id, connection):
        self.channel_id = channel_id
        self.connection = connection

    def run(self):
        # Ask the IRC server for a list of channel mods
        self.connection.send('CAP REQ :twitch.tv/commands\r\n'.encode())
        irc.send_message(self.connection, '#ibunnib', '.mods')

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

                    # If data is of type NOTICE
                    if line[1] == 'NOTICE':
                        msg = irc.get_message(line)

                        # If the notice is the moderator list
                        if 'The moderators of this room are:' in msg:
                            # Store the list of mods
                            print('> Reading moderator list...')
                            users = msg.split(':')[1]
                            users = users.split(',')
                            self.mods = [user.lstrip() for user in users]
                            # Add the channel owner to list of mods
                            self.mods.append(config.channel)
                            print(f'> Moderators: {self.mods}')

                    # If data is a regular chat message
                    if line[1] == 'PRIVMSG':
                        # Get message details
                        sender = irc.get_sender(line)
                        msg = irc.get_message(line)
                        channel = line[2]

                        # If sender is a moderator
                        if sender in self.mods:
                            print(f'[M] {sender}: {msg}')
                        else:
                            print(f'{sender}: {msg}')

                        # !hi
                        if msg.split()[0] == '!hi':
                            irc.send_message(self.connection, channel, f'Hi {sender}! <3')

                        # !title
                        if msg.split()[0] == '!title' and sender in self.mods:
                            title = msg.split('!title')[1].lstrip()
                            print(f'> Changing stream title to "{title}"')
                            twitch.set_stream_title(self.channel_id, title)
                            irc.send_message(self.connection, channel, f'Set stream title to "{title}"')

            except socket.error:
                print('> SOCKET ERROR')
            except socket.timeout:
                print('> SOCKET TIMEOUT')

class NewFollowerManager():
    def __init__(self, channel_id, connection):
        self.channel_id = channel_id
        self.connection = connection

    def run(self):
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
