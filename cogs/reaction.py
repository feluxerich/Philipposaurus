from discord.ext.commands import Cog
from discord.utils import get
from utils import *
from discord import Member, Guild


class Reaction(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = return_config()['guilds'][str(payload.guild_id)]
        if guild['channels']['rules'] and payload.channel_id == guild['channels']['rules'] \
                and str(payload.emoji) in guild['rule']:
            await payload.member.add_roles(
                get(
                    payload.member.guild.roles, id=guild['rule'][str(payload.emoji)]
                )
            )
        if guild['channels']['roles'] and payload.channel_id == guild['channels']['roles'] \
                and str(payload.emoji) in guild['reactions']:
            await payload.member.add_roles(
                get(
                    payload.member.guild.roles, id=guild['reactions'][str(payload.emoji)]
                )
            )

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = return_config()['guilds'][str(payload.guild_id)]
        server: Guild = self.client.get_guild(payload.guild_id)
        member: Member = server.get_member(payload.user_id)
        if guild_id['channels']['rules'] and payload.channel_id == guild_id['channels']['rules'] \
                and str(payload.emoji) in guild_id['rule']:
            await member.remove_roles(
                get(
                    member.guild.roles, id=guild_id['rule'][str(payload.emoji)]
                )
            )
        if guild_id['channels']['roles'] and payload.channel_id == guild_id['channels']['roles'] \
                and str(payload.emoji) in guild_id['reactions']:
            await member.remove_roles(
                get(
                    member.guild.roles, id=guild_id['reactions'][str(payload.emoji)]
                )
            )


def setup(client):
    client.add_cog(Reaction(client))
