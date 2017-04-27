import socket
import re

import irc

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
                print('SOCKET ERROR')
            except socket.timeout:
                print('SOCKET TIMEOUT')
