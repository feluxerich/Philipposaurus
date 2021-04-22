from json import load, dump
from errors import *
from os.path import isfile


def is_config(function):
    def wrapper(*args, **kwargs):
        if isfile('./configs.json'):
            return function(*args, **kwargs)
        else:
            raise NoConfigFileFound
    return wrapper


@is_config
def return_config():
    with open('./configs.json') as file:
        return load(file)


@is_config
def write_config(data):
    with open('./configs.json', 'w') as file:
        dump(data, file, indent=4)


def create_config():
    default_config = {
        "token": "",
        "presence": [],
        "guilds": {},
    }
    if not isfile('./configs.json'):
        with open('configs.json', 'w') as file:
            dump(default_config, file, indent=4)


@is_config
def reset_guild(guild_id: str):
    data = return_config()
    default_guild = {
        "rule": {},
        "reactions": {},
        "channels": {
            "new_talk": None,
            "new_private_talk": None,
            "rules": None,
            "roles": None
        }
    }
    data['guilds'][guild_id] = default_guild
    write_config(data)


@is_config
def create_guild(guild_id: str):
    data = return_config()
    default_guild = {
        "rule": {},
        "reactions": {},
        "channels": {
            "new_talk": None,
            "new_private_talk": None,
            "rules": None,
            "roles": None
        }
    }
    if guild_id not in data['guilds']:
        data['guilds'][guild_id] = default_guild
        write_config(data)
