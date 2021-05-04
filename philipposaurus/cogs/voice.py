from discord.ext.commands import Cog, command
from discord import PermissionOverwrite, Member
from utils import *
from errors import OnlyPrivateChannel


class Voice(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            channels = return_config()['guilds'][str(after.channel.guild.id)]['channels']
            if after.channel.id == channels['new_talk']:
                talk_sum = 1
                for channel in after.channel.guild.voice_channels:
                    if channel.name.startswith('Public Talk '):
                        talk_sum += 1
                await member.move_to(
                    await after.channel.guild.create_voice_channel(
                        name=f'Public Talk {talk_sum}',
                        category=after.channel.category,
                        overwrites={
                            member: PermissionOverwrite(
                                mute_members=True,
                                deafen_members=True,
                                manage_channels=True
                            )
                        }
                    )
                )
            if after.channel.id == channels['new_private_talk']:
                private_talk_sum = 1
                for channel in after.channel.guild.voice_channels:
                    if channel.name.startswith('Private Talk '):
                        private_talk_sum += 1
                await member.move_to(
                    await after.channel.guild.create_voice_channel(
                        name=f'Private Talk {private_talk_sum}',
                        category=after.channel.category,
                        overwrites={
                            after.channel.guild.default_role: PermissionOverwrite(
                                connect=False, view_channel=False
                            ),
                            member: PermissionOverwrite(
                                connect=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                view_channel=True
                            )
                        }
                    )
                )
        if before.channel:
            if before.channel.name.startswith('Public Talk ') or before.channel.name.startswith('Private Talk '):
                if len(before.channel.members) <= 0:
                    await before.channel.delete()

    @command(aliases=['vi', 'invite'], description='Invites a member to a private voice channel. If the member has'
                                                   'deactivated direct messages from other users he gets the'
                                                   'permissions to see the channel')
    async def voice(self, ctx, member: Member):
        if ctx.author.voice and ctx.author.voice.channel.name.startswith('Private Talk '):
            await ctx.author.voice.channel.set_permissions(
                member,
                connect=True,
                view_channel=True,
                speak=True
            )
            try:
                await member.send(
                    await ctx.author.voice.channel.create_invite(
                        max_uses=1,
                        max_age=600
                    )
                )
            except Exception as error:
                raise error
        else:
            raise OnlyPrivateChannel(ctx.author.voice.channel.name)


def setup(client):
    client.add_cog(Voice(client))
