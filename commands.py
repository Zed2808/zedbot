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
    cmds = [(cmd[1], cmd[1].trigger) for cmd in class_list if cmd[1].trigger != ['']]
    return cmds

def get_names():
    command_names = [cmd[1] for cmd in get_commands()]
    command_names = ['/'.join(cmd) for cmd in command_names]
    command_names = ' '.join(command_names)
    return command_names

# Base Command class to inherit from, not an actual command
class Command():
    trigger = ['']

    def execute(connection, channel, sender, message, mod):
        return 'Base message'

# Sends list of available commands
class Help(Command):
    trigger = ['!help']

    def execute(connection, channel, sender, message, mod):
        irc.send_message(connection, channel, f'Commands: {get_names()}')

# Greet the sender in chat
class Hi(Command):
    trigger = ['!hi', '!hello']

    def execute(connection, channel, sender, message, mod):
        irc.send_message(connection, channel, f'Hi {sender}! <3')

# Change the title of the stream (mod only)
class Title(Command):
    trigger = ['!title', '!status']

    def execute(connection, channel, sender, message, mod):
        if mod:
            channel_id = twitch.get_channel_id(config.channel)
            title = message.replace('!title ', '')
            print(f'Changing stream title to "{title}"')
            twitch.set_stream_title(channel_id, title)
            irc.send_message(connection, channel, f'Set stream title to "{title}"')

# Quote an Overwatch character
class Quote(Command):
    trigger = ['!quote', '!genji', '!hanzo', '!mercy']

    def execute(connection, channel, sender, message, mod):
        character = message.split()[0].lstrip('!')

        # If "!quote", pick a totally random quote
        if character == 'quote':
            quote_list = [quotes.quotes[key] for key in quotes.quotes]
            quote_list = [quote for char_quotes in quote_list for quote in char_quotes]
            quote = random.choice(quote_list)
            print('Quoting random character')
        else:
            quote = random.choice(quotes.quotes[character])
            print(f'Quoting "{character}"')

        irc.send_message(connection, channel, quote)
