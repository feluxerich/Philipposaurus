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
                description='voice | channel | reactions | onjoin',
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

    @set.group(description='Join a channel you want to set then use a subcommand')
    async def voice(self, ctx):
        if ctx.invoked_subcommand is None:
            voice_embed = Embed(
                title='Settings',
                description=f'public | private',
                color=colour()
            )
            await ctx.send(embed=voice_embed)

    @voice.command(description='Set a channel to the new_talk channel')
    async def public(self, ctx):
        if ctx_voice := ctx.author.voice:
            data = return_config()
            if str(ctx.guild.id) not in data['guilds']:
                create_guild(str(ctx.guild.id))
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['new_talk'] = ctx_voice.channel.id
            write_config(data)
        else:
            raise NoUserVoiceFound
        set_voice_embed = Embed(
            title='Settings',
            description=f'The channel `{ctx_voice.channel.name}` '
                        f'was successfully set to the new-public-channel',
            color=colour()
        )
        await ctx.send(embed=set_voice_embed)

    @voice.command(description='Set a channel to the new_private_talk channel')
    async def private(self, ctx):
        if ctx_voice := ctx.author.voice:
            data = return_config()
            if str(ctx.guild.id) not in data['guilds']:
                create_guild(str(ctx.guild.id))
            data = return_config()
            data['guilds'][str(ctx.guild.id)]['channels']['new_private_talk'] = ctx_voice.channel.id
            write_config(data)
        else:
            raise NoUserVoiceFound
        set_voice_embed = Embed(
            title='Settings',
            description=f'The channel `{ctx_voice.channel.name}` '
                        f'was successfully set to the new-private-channel',
            color=colour()
        )
        await ctx.send(embed=set_voice_embed)

    @set.group(description='Set a channel to the rule or the role channel')
    async def text(self, ctx):
        if ctx.invoked_subcommand is None:
            set_channel_embed = Embed(
                title='Settings',
                description='rule | role',
                color=colour()
            )
            await ctx.send(embed=set_channel_embed)

    @text.command(description='Set the rule channel')
    async def rule(self, ctx, channel: TextChannel):
        data = return_config()
        data['guilds'][str(ctx.guild.id)]['channels']['rules'] = channel.id
        write_config(data)
        set_rule_embed = Embed(
            title='Settings',
            description=f'The channel `{channel.name}` was successfully set to the rule-Channel',
            color=colour()
        )
        await ctx.send(embed=set_rule_embed)

    @text.command(description='Set the self-role channel')
    async def role(self, ctx, channel: TextChannel):
        data = return_config()
        data['guilds'][str(ctx.guild.id)]['channels']['roles'] = channel.id
        write_config(data)
        set_rule_embed = Embed(
            title='Settings',
            description=f'The channel `{channel.name}` was successfully set to the rule-Channel',
            color=colour()
        )
        await ctx.send(embed=set_rule_embed)

    @set.group(description='Add or remove reactions to reaction role')
    async def reaction(self, ctx):
        if ctx.invoked_subcommand is None:
            set_reaction_embed = Embed(
                title='Settings',
                description='add | remove',
                color=colour()
            )
            await ctx.send(embed=set_reaction_embed)

    @reaction.group(description='Add reactions to rule or role')
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            add_embed = Embed(
                title='Settings',
                description='rule | role',
                color=colour()
            )
            await ctx.send(embed=add_embed)

    @add.command(description='Add reaction rule')
    async def rule(self, ctx, emoji, role: Role):
        reaction_role = ReactionRole(
            guild=ctx.guild,
            emoji=emoji,
            role=role,
            rule=True
        )
        reaction_role.add()
        rule_add_embed = Embed(
            title='Settings',
            description=f'The reaction rule-reaction-role {role.mention} was added with emoji {emoji}',
            color=colour()
        )
        await ctx.send(embed=rule_add_embed)

    @add.command(description='Add reaction role')
    async def role(self, ctx, emoji, role: Role):
        reaction_role = ReactionRole(
            guild=ctx.guild,
            emoji=emoji,
            role=role,
            rule=False
        )
        reaction_role.add()
        role_add_embed = Embed(
            title='Settings',
            description=f'The reaction role-reaction-role {role.mention} was added with emoji {emoji}',
            color=colour()
        )
        await ctx.send(embed=role_add_embed)

    @reaction.group(description='Remove reactions from rule or role')
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            remove_embed = Embed(
                title='Settings',
                description='rule | rule',
                color=colour()
            )
            await ctx.send(embed=remove_embed)

    @remove.command(description='Remove a rule reaction')
    async def rule(self, ctx, emoji, role: Role):
        reaction_role = ReactionRole(
            guild=ctx.guild,
            emoji=emoji,
            role=role,
            rule=True
        )
        reaction_role.remove()
        rule_remove_embed = Embed(
            title='Settings',
            description=f'The reaction rule-reaction-role {role.mention} was removed from emoji {emoji}',
            color=colour()
        )
        await ctx.send(embed=rule_remove_embed)

    @remove.command(description='Remove a self-role reaction')
    async def role(self, ctx, emoji, role: Role):
        reaction_role = ReactionRole(
            guild=ctx.guild,
            emoji=emoji,
            role=role,
            rule=False
        )
        reaction_role.remove()
        role_remove_embed = Embed(
            title='Settings',
            description=f'The reaction role-reaction-role {role.mention} was removed from emoji {emoji}',
            color=colour()
        )
        await ctx.send(embed=role_remove_embed)

    # TODO: implement a list all reaction roles command
    # TODO: make an command for listing all channels and reactions


def setup(client):
    client.add_cog(Settings(client))
