from discord.ext.commands import Cog, command
from discord import Embed
from requests import get
from asyncio import sleep
from utils import colour


class Joke(Cog):
    def __init__(self, client):
        self.client = client

    @command(description='Sends a random Joke. After ten seconds there will appear the pointe')
    async def joke(self, ctx, joke_type=None):
        joke_embed = Embed(
            title='Joke',
            color=colour()
        )
        joke = None
        joke_types = ['general', 'knock-knock', 'programming']
        if joke_type and joke_type.lower() in joke_types:
            joke = get(f'https://official-joke-api.appspot.com/jokes/{joke_type}/random')
        if not joke_type:
            joke = get('https://official-joke-api.appspot.com/jokes/random').json()
        joke_embed.description = joke['setup']
        sent_message = await ctx.send(embed=joke_embed)
        await sleep(10)
        joke_embed.description = joke['punchline']
        await sent_message.edit(embed=joke_embed, delete_after=10)


def setup(client):
    client.add_cog(Joke(client))
