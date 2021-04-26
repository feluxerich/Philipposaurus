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
        role: Role = get(guild.roles, id=data['guilds'][str(guild.id)]['on_join_role'])
        await member.add_roles(role)


def setup(client):
    client.add_cog(Events(client))
