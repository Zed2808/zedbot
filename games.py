import pickle
import random
import collections

import games_config

save_name = 'credits.p'
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

def save():
    pickle.dump(credits, open(save_name, 'wb'))

def balance(user):
    # Create record for user if it doesn't exist yet
    if user not in credits.keys():
        credits[user] = games_config.starting_credits
        print(f'Created credits record for {user}')

    balance = credits[user]
    print(f'Read balance of {user} ({balance})')

    return balance

def set_balance(user, balance):
    credits[user] = int(balance)
    print(f'Set balance of {user} to {balance}')

    save()
    print(f'Wrote {user}\'s balance to {save_name}')

def spin_slots(user):
    messages = []

    # Take credits from user
    credits[user] -= games_config.slots_cost
    save()
    print(f'Removed {games_config.slots_cost} credits from {user}')
    messages.append(f'{user} spent {games_config.slots_cost} credits to spin')

    # Spin reels
    emotes = [random.choice(games_config.slots_emotes) for x in range(games_config.slots_reels)]
    emotes_message = ' '.join(emotes)
    print(f'{user} spun {emotes_message}')
    messages.append(emotes_message)

    # Count frequency of each emote
    counter = list(collections.Counter(emotes).values())

    # Give rewards
    reward = 0
    for freq in counter:
        # Add reward if payout exists for frequency
        if freq in games_config.slots_rewards:
            reward += games_config.slots_rewards[freq]

    # If no reward, special message
    if reward == 0:
        messages.append(f'Good luck next time {user}!')
    # Else, give reward (and initial wager)
    else:
        credits[user] += (reward + games_config.slots_cost)
        save()
        messages.append(f'{user} won {reward}!')

    print(f'{user} won {reward} credits')

    return messages
