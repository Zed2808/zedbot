import inspect
import sys
import random

import config
import irc
import twitch
import quotes

# Return a list of commands along with their trigger words
# Example: [(<class 'commands.Hi'>, '!hi'), (<class 'commands.Title'>, '!title')]
def get_commands():
    class_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    cmds = [(cmd[1], cmd[1].trigger()) for cmd in class_list if cmd[1].trigger() != '']
    return cmds

# Base Command class to inherit from, not an actual command
class Command():
    def trigger():
        return ''

    def execute(connection, channel, sender, message, mod):
        return 'Base message'

# Greet the sender in chat
class Hi(Command):
    def trigger():
        return ['!hi', '!hello']

    def execute(connection, channel, sender, message, mod):
        irc.send_message(connection, channel, f'Hi {sender}! <3')

# Change the title of the stream (mod only)
class Title(Command):
    def trigger():
        return ['!title', '!status']

    def execute(connection, channel, sender, message, mod):
        if mod:
            channel_id = twitch.get_channel_id(config.channel)
            title = message.replace('!title ', '')
            print(f'Changing stream title to "{title}"')
            twitch.set_stream_title(channel_id, title)
            irc.send_message(connection, channel, f'Set stream title to "{title}"')

# Quote an Overwatch character
class Quote(Command):
    def trigger():
        return ['!genji', '!hanzo', '!mercy']

    def execute(connection, channel, sender, message, mod):
        message = message.split()
        character = message[0].lstrip('!')
        print(f'Quoting "{character}"')
        quote = random.choice(quotes.quotes[character])
        irc.send_message(connection, channel, quote)
