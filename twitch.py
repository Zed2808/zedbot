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

def get_follower_ids(channel_id):
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': config.client_id}

    url = f'https://api.twitch.tv/kraken/channels/{channel_id}/follows'

    r = requests.get(url, headers=headers)

    data = json.loads(r.text)

    return [follower['user']['_id'] for follower in data['follows']]

def get_username_by_id(id):
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': config.client_id}

    url = f'https://api.twitch.tv/kraken/users/{id}'

    r = requests.get(url, headers=headers)

    data = json.loads(r.text)

    return data['display_name']

def set_stream_title(channel_id, title):
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': config.client_id,
               'Authorization': 'OAuth ' + config.oauth,
               'Content-Type': 'application/json'}

    url = f'https://api.twitch.tv/kraken/channels/{channel_id}'

    data = json.dumps({'channel': {'status': title}})

    r = requests.put(url, headers=headers, data=data)
