import socket
import re
import time
import random

import config
import irc
import commands
import twitch
import quotes

class IRCManager():
    def __init__(self, channel_id, connection):
        self.channel_id = channel_id
        self.connection = connection

        # Get the list of commands
        self.command_list = commands.get_commands()

        # Print available commands
        command_names = [cmd[1] for cmd in self.command_list]
        command_names = ['/'.join(cmd) for cmd in command_names]
        command_names = ' '.join(command_names)
        print(f'Commands: {command_names}')

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
                            print('Reading moderator list...')
                            users = msg.split(':')[1]
                            users = users.split(',')
                            self.mods = [user.lstrip() for user in users]
                            # Add the channel owner to list of mods
                            self.mods.append(config.channel)

                            # Print list of mods
                            mod_names = ' '.join(self.mods)
                            print(f'Moderators: {mod_names}')

                    # If data is a regular chat message
                    if line[1] == 'PRIVMSG':
                        # Get message details
                        sender = irc.get_sender(line)
                        msg = irc.get_message(line)
                        channel = line[2]

                        # Determine if sender is mod in channel
                        mod_status = sender in self.mods

                        # If sender is a moderator
                        if mod_status:
                            print(f'> [M] {sender}: {msg}')
                        else:
                            print(f'> {sender}: {msg}')

                        # Use first word as command
                        cmd = msg.split()[0]

                        # Iterate through each command
                        for command in self.command_list:
                            # If the command's trigger word matches the first word in the message
                            if cmd in command[1]:
                                # Execute the matching command
                                command[0].execute(self.connection, channel, sender, msg, mod_status)

            except socket.error:
                print('SOCKET ERROR')
            except socket.timeout:
                print('SOCKET TIMEOUT')

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
                    print(f'New follower: {follower_name}')

                    # Welcome new follower in chat
                    irc.send_message(self.connection, '#' + config.channel, f'Welcome {follower_name}! <3')

            # Save current followers to check against
            self.followers = current_followers

            time.sleep(5)
