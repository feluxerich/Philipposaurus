from discord.ext.commands import Cog
from discord.utils import get
from utils import *
from discord import Guild


class Events(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_member_join(self, member):
        data = return_config()
        guild: Guild = member.guild
        if role_id := data['guilds'][str(guild.id)]['on_join_role']:
            role: Role = get(guild.roles, id=role_id)
            await member.add_roles(role)

    @Cog.listener()
    async def on_guild_join(self, guild):
        create_guild(str(guild.id))


def setup(client):
    client.add_cog(Events(client))
