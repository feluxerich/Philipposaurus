from utils import *
from discord.ext.commands import Bot, when_mentioned_or
from os import listdir
from discord import Embed, Intents

client = Bot(command_prefix=when_mentioned_or('.'), intents=Intents.all())

create_config()


@client.event
async def on_ready():
    print(f'Bot is now ready with ID: {client.user.id}')


@client.command()
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
        description=f'**Successful**\n{successful}**Failed**\n{failed}',
        color=0x00ff00
    )
    # TODO: Do the successful and the failed cog imports in embed-fields when it's working again
    await ctx.send(embed=reload_embed, delete_after=10)


for file in listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded {file}')
    else:
        print(f'Not a python file: {file}')

client.run(return_config()['token'])
