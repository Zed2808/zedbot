import pickle

save_name = 'credits.p'
starting_credits = 1000
credits = {}

def init_games():
    global credits

    # Try to open and read the save file
    try:
        with open(save_name, 'rb') as save_file:
            print(f'Reading credit balances from {save_name}...')
            credits = pickle.load(save_file)
    # If we can't (the file doesn't exist or is empty) credits = {} anyways
    except:
        print(f'Could not read from {save_name}')

def balance(user):
    # Create record for user if it doesn't exist yet
    if user not in credits.keys():
        credits[user] = starting_credits
        print(f'Created credits record for {user}')

    balance = credits[user]
    print(f'Read balance of {user} ({balance})')

    return balance

def set_balance(user, balance):
    credits[user] = int(balance)
    print(f'Set balance of {user} to {balance}')

    pickle.dump(credits, open(save_name, 'wb'))
    print(f'Wrote {user}\'s balance to {save_name}')
