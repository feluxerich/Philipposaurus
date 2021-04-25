from utils import *
from discord.ext.commands import Bot, when_mentioned_or
from os import listdir
from discord import Embed, Intents, Game, Status
from asyncio import sleep

client = Bot(command_prefix=when_mentioned_or('.'), intents=Intents.all())

create_config()


@client.event
async def on_ready():
    print(f'Bot is now ready with ID: {client.user.id}')
    for guild in client.guilds:
        create_guild(str(guild.id))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        for status in return_config()['presence']:
            await client.change_presence(activity=Game(status), status=Status.online)
            await sleep(5)


@client.command()
async def reload(ctx):
    """This Command reloads the bot"""
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
        description=f'**Successful**\n{successful}**Failed**\n{failed}',
        color=0x00ff00
    )
    # TODO: Do the successful and the failed cog imports in embed-fields when it's working again
    await ctx.send(embed=reload_embed, delete_after=10)


@client.event
async def on_guild_join(guild):
    create_guild(str(guild.id))


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
