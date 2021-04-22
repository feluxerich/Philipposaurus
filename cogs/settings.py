from discord.ext.commands import Cog, command
from utils import *
from errors import NoUserVoiceFound
from re import search
from discord import TextChannel, Embed, Role, Emoji


class Settings(Cog):
    def __init__(self, client):
        self.client = client

    @command()
    async def set_voice(self, ctx, *, voice_type):
        """Join the channel which you want to set to the new talk or to the new private talk channel
        then type this command and which type (new talk | new private talk) then this channel will be set
        to this"""
        if ctx.author.voice:
            voice_type = 'new_talk' if search('new[- _]talk', voice_type.lower()) else 'new_private_talk'
            data = return_config()
            if str(ctx.guild.id) not in data['guilds']:
                create_guild(str(ctx.guild.id))
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels'][voice_type] = ctx.author.voice.channel.id
            write_config(data)
        else:
            raise NoUserVoiceFound
        set_voice_embed = Embed(
            title='Settings',
            description=f'The channel `{ctx.author.voice.channel.name}` '
                        f'was successfully set to a `{voice_type}`-Channel',
            color=0x00ff00
        )
        await ctx.send(embed=set_voice_embed)

    @command()
    async def set_channel(self, ctx, channel_type, channel: TextChannel):
        """Set a channel to the rule or the autorole channel. Available channel types: rule | role"""
        if channel_type.lower().startswith('rule'):
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['rules'] = channel.id
            write_config(data)
        elif channel_type.lower().startswith('role'):
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['roles'] = channel.id
            write_config(data)
        else:
            raise WrongChannelType
        set_channel_embed = Embed(
            title='Settings',
            description=f'The channel `{channel}` was successfully set to a `{channel_type}`-Channel',
            color=0x00ff00
        )
        await ctx.send(embed=set_channel_embed)

    @command()
    async def set_reactions(self, ctx, emoji: Emoji, role: Role, rule='false'):
        """Add reactions to reaction role or to the rule"""
        data = return_config()
        data['guilds'][str(ctx.guild.id)]['rule' if rule.lower() == 'true' else 'reactions'][str(emoji)] = role.id
        write_config(data)


def setup(client):
    client.add_cog(Settings(client))
