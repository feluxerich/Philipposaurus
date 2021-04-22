from discord.ext.commands import Cog, command
from utils import *
from errors import NoUserVoiceFound
from re import search


class Settings(Cog):
    def __init__(self, client):
        self.client = client

    @command()
    async def set_voice(self, ctx, *, voice_type):
        if ctx.author.voice:
            voice_type = 'new_talk' if search('new[- _]talk', voice_type.lower()) else 'new_private_talk'
            data = return_config()
            if str(ctx.guild.id) not in data['guilds']:
                reset_guild(str(ctx.guild.id))
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels'][voice_type] = ctx.author.voice.channel.id
            write_config(data)


def setup(client):
    client.add_cog(Settings(client))
