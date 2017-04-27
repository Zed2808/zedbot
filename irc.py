import config

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
