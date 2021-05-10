from discord.ext.commands import Cog, group, has_guild_permissions
from utils import *
from errors import NoUserVoiceFound
from discord import TextChannel, Embed, Role


class Settings(Cog):
    def __init__(self, client):
        self.client = client

    @group(description='Set some channels or reactions for your server')
    @has_guild_permissions(manage_channels=True)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            settings_embed = Embed(
                title='Settings',
                description='voice | text | reaction | onjoin',
                color=colour()
            )
            await ctx.send(embed=settings_embed)

    @set.command(description='Set the role which should be given to a new member')
    async def onjoin(self, ctx, role: Role):
        data = return_config()
        data['guilds'][str(ctx.guild.id)]['on_join_role'] = role.id
        write_config(data)
        on_join_embed = Embed(
            title='Settings',
            description=f'On Member Join Role was set successful to {role.name}',
            color=colour()
        )
        await ctx.send(embed=on_join_embed)

    @set.command(description='Join a channel you want to set then use a subcommand')
    async def voice(self, ctx, channel_type=None):
        voice_embed = Embed(
            title='Settings',
            color=colour()
        )
        if channel_type is None:
            voice_embed.description = 'public | private'
        elif channel_type.lower() == 'public':
            if ctx_voice := ctx.author.voice:
                data = return_config()
                if str(ctx.guild.id) not in data['guilds']:
                    create_guild(str(ctx.guild.id))
                data = return_config()
                data['guilds'][str(ctx.guild.id)]['channels']['new_talk'] = ctx_voice.channel.id
                write_config(data)
            else:
                raise NoUserVoiceFound
            voice_embed.description = f'The channel `{str(ctx_voice.channel.name)}` was successfully set to the ' \
                                      f'new-public-channel'
        elif channel_type.lower() == 'private':
            if ctx_voice := ctx.author.voice:
                data = return_config()
                if str(ctx.guild.id) not in data['guilds']:
                    create_guild(str(ctx.guild.id))
                data = return_config()
                data['guilds'][str(ctx.guild.id)]['channels']['new_private_talk'] = ctx_voice.channel.id
                write_config(data)
            else:
                raise NoUserVoiceFound
            voice_embed.description = f'The channel `{str(ctx_voice.channel.name)}` was successfully set to the ' \
                                      f'new-private-channel'
        else:
            voice_embed.description = 'Invalid input'
        await ctx.send(embed=voice_embed)

    @set.command(description='Set a channel to the rule or the role channel')
    async def text(self, ctx, channel_type=None, channel: TextChannel = None):
        set_rule_embed = Embed(
            title='Settings',
            color=colour()
        )
        if channel_type is None:
            set_rule_embed.description = 'rule | role'
        elif channel_type.lower() == 'rule':
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['rules'] = channel.id
            write_config(data)
            set_rule_embed.description = f'The channel `{channel.name}` was successfully set to the rule-Channel'
        elif channel_type.lower() == 'role':
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['roles'] = channel.id
            write_config(data)
            set_rule_embed.description = f'The channel `{channel.name}` was successfully set to the role-Channel'
        else:
            set_rule_embed.description = 'Invalid input'
        await ctx.send(embed=set_rule_embed)

    @set.command(description='Add or remove reactions to reaction role')
    async def reaction(self, ctx, operation=None, reaction_type=None, emoji=None, role: Role = None):
        reaction_embed = Embed(
            title='Settings',
            color=colour()
        )
        if operation is None:
            reaction_embed.description = 'add | remove'
        elif operation.lower() == 'add':
            if reaction_type is None:
                reaction_embed.description = 'rule | role'
            elif reaction_type.lower() == 'rule':
                reaction_role = ReactionRole(
                    guild=ctx.guild,
                    emoji=emoji,
                    role=role,
                    rule=True
                )
                reaction_role.add()
                reaction_embed.description = f'The reaction rule-reaction-role {role.mention} was ' \
                                             f'added with emoji {emoji}'
            elif reaction_type.lower() == 'role':
                reaction_role = ReactionRole(
                    guild=ctx.guild,
                    emoji=emoji,
                    role=role,
                    rule=False
                )
                reaction_role.add()
                reaction_embed.description = f'The reaction role-reaction-role {role.mention} was ' \
                                             f'added with emoji {emoji}'
        elif operation.lower() == 'remove':
            if reaction_type is None:
                reaction_embed.description = 'rule | role'
            elif reaction_type.lower() == 'rule':
                reaction_role = ReactionRole(
                    guild=ctx.guild,
                    emoji=emoji,
                    role=role,
                    rule=True
                )
                reaction_role.remove()
                reaction_embed.description = f'The reaction rule-reaction-role {role.mention} was ' \
                                             f'added with emoji {emoji}'
            elif reaction_type.lower() == 'role':
                reaction_role = ReactionRole(
                    guild=ctx.guild,
                    emoji=emoji,
                    role=role,
                    rule=False
                )
                reaction_role.remove()
                reaction_embed.description = f'The reaction role-reaction-role {role.mention} was ' \
                                             f'added with emoji {emoji}'
        else:
            reaction_embed.description = 'Invalid input'
        await ctx.send(embed=reaction_embed)

    # TODO: implement a list all reaction roles command
    # TODO: make an command for listing all channels and reactions


def setup(client):
    client.add_cog(Settings(client))
