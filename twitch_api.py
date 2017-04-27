import requests
import json

import config

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
