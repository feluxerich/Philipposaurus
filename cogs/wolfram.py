from discord.ext.commands import Cog, command
from discord import Embed
from wolframalpha import Client
from utils import *


class Wolfram(Cog):
    def __init__(self, client):
        self.client = client
        self.data = return_config()

    @command(aliases=['wolfram', 'alpha'], description='Send a request for example to calculate '
                                                       'something with the Wolframalpha API')
    async def wolf(self, ctx):
        client = Client(self.data['api_keys']['wolframalpha'])
        wait_embed = Embed(
            title='Wolfram ALPHA',
            color=colour()
        )
        wait_embed.description = 'Please type what you want to get from the API. ' \
                                 'Your request will be timed out in 5 minutes'
        sent_message = await ctx.send(embed=wait_embed)
        resp = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=600)
        response = client.query(resp.content)
        output = next(response.results).text
        wait_embed.description = output
        await resp.delete()
        await sent_message.edit(embed=wait_embed)


def setup(client):
    client.add_cog(Wolfram(client))
