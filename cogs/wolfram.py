from discord.ext.commands import Cog, command
from discord import Embed
from utils import *
from aiohttp import ClientSession


class Wolfram(Cog):
    def __init__(self, client):
        self.client = client
        self.data = return_config()

    @command(aliases=['wolfram', 'alpha', 'calc', 'calculate'], description='Send a request for example to calculate '
                                                                            'something with the Wolframalpha API')
    async def wolf(self, ctx):
        wait_embed = Embed(
            title='Wolfram ALPHA',
            color=colour()
        )
        wait_embed.description = 'Please type what you want to get from the API. ' \
                                 'Your request will be timed out in 5 minutes'
        sent_message = await ctx.send(embed=wait_embed)
        resp = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=600)
        keys = {
            '+': 'plus',
            '-': 'minus',
            '**': '^',
            '*': 'multi',
            '/': 'div',
            ' ': '+'
        }
        inpt = resp.content
        for key in keys:
            inpt = inpt.replace(key, keys[key])
        wait_embed.description = None
        url = f"https://api.wolframalpha.com/v2/result?appid={self.data['api_keys']['wolframalpha']}&i={inpt}%3F"
        async with ClientSession() as session:
            async with await session.get(url) as response:
                output = await response.text()
        wait_embed.add_field(
            name='Input',
            value=resp.content, inline=False
        )
        wait_embed.add_field(
            name='Output',
            value=output.replace('{', '').replace('}', '').replace('->', ' = '), inline=False
        )
        await resp.delete()
        await sent_message.edit(embed=wait_embed)


def setup(client):
    client.add_cog(Wolfram(client))
