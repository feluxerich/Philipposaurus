from json import load, dump
from errors import *
from os.path import isfile
from discord import Role, Guild
from random import choice
from pydantic import BaseModel


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
        "api_keys": {
            "hypixel": "",
            "osu": ""
        },
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
        "on_join_role": None,
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


class ReactionRole:
    def __init__(self, guild: Guild, emoji, role: Role, rule: bool = False):
        self.guild = guild
        self.emoji = emoji
        self.role = role
        self.rule = rule
        self.data = return_config()

    def add(self):
        reaction_type = 'rule' if self.rule is True else 'reactions'
        self.data['guilds'][str(self.guild.id)][reaction_type][str(self.emoji)] = self.role.id
        write_config(self.data)

    def remove(self):
        reaction_type = 'rule' if self.rule is True else 'reactions'
        try:
            del self.data['guilds'][str(self.guild.id)][reaction_type][str(self.emoji)]
        except KeyError:
            pass
        write_config(self.data)

    # TODO: make a send_command function


colours = [
    0x0f4c75,
    0x801336,
    0x801336,
    0x115173,
    0x00454a,
    0x581845,
    0x45056e,
    0x5a082d,
    0x055e68
]


def colour():
    return choice(colours)


def return_accounts():
    with open('accounts.json') as file:
        return load(file)


class User(BaseModel):
    discord_id: int
    discord_name: str
    minecraft_id: str
    minecraft_name: str
