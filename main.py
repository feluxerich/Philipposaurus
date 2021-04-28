from utils import *
from discord.ext.commands import Bot, when_mentioned_or
from os import listdir
from discord import Embed, Intents, Game, Status
from asyncio import sleep

client = Bot(
    command_prefix=when_mentioned_or('.'),
    intents=Intents.all(),
    help_command=None
)

create_config()


@client.event
async def on_ready():
    print(f'Bot is now ready with ID: {client.user.id}')
    for guild in client.guilds:
        create_guild(str(guild.id))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        count = 0
        for _ in client.guilds:
            count += 1
        for status in return_config()['presence']:
            status = status.replace('{servers}', str(count))
            await client.change_presence(activity=Game(status), status=Status.online)
            await sleep(5)


@client.command(name='help', aliases=['h', 'commands'])
async def command_list(ctx, *, cog_or_command=None):
    cogs = [f'{cog}' for cog in client.cogs.keys()]
    just_events = ['Reaction', 'Events']
    for removable in just_events:
        cogs.remove(removable)
    help_embed = Embed(
        title='Help',
        color=0x00ffff
    )
    if cog_or_command is None:
        for cog in cogs:
            commands = ""
            for command in client.get_cog(cog).get_commands():
                help_command = f'{command.name} - {command.description}\n'
                if len(help_command) >= 60:
                    commands += f'{help_command[:57]}...\n'
                else:
                    commands += help_command
            # this version does not display the subcommands
            # if you want to display them, do this:
            # for command in client.get_cog(cog).walk_commands():
            #   ...
            help_embed.add_field(name=cog, value=str(commands), inline=False)
        help_embed.add_field(name='No Category', value='help - Shows this help\nreload - Reloads the bot\n\n'
                                                       'Type `help <cog | command>` for specificated help')
    else:
        if cog_or_command in client.cogs:
            commands = ''
            for command in client.get_cog(cog_or_command).get_commands():
                commands += f'`{command.name}` - {command.description}\n'
            help_embed.add_field(name=cog_or_command, value=commands)
        elif command := client.get_command(cog_or_command):
            command = f'`{command.name}` - {command.description}'
            help_embed.add_field(name=cog_or_command.capitalize(), value=command)
        else:
            help_embed.add_field(name='Error', value='This is not a category or a command')
    help_embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=help_embed)


@client.command(description='Reloads the bot')
async def reload(ctx):
    successful = str()
    failed = str()
    for file in listdir('./cogs'):
        if file.endswith('.py'):
            client.reload_extension(f'cogs.{file[:-3]}')
            successful += f'Loaded `{file}`\n'
        else:
            failed += f'Not a python file: `{file}`'
    reload_embed = Embed(
        title='Reload',
        color=0x00ff00
    )
    reload_embed.add_field(name='Successful', value=successful, inline=False)
    reload_embed.add_field(name='Failed', value=failed, inline=False)
    await ctx.send(embed=reload_embed)


# TODO: uncomment this error handler
# @client.event
# async def on_command_error(ctx, error):
#     error_embed = Embed(
#         title='Error',
#         description=error,
#         color=0xff0000
#     )
#     await ctx.send(embed=error_embed)


for file in listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded {file}')
    else:
        print(f'Not a python file: {file}')

client.run(return_config()['token'])
