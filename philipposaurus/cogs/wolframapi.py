from discord.ext.commands import Cog, command
from discord import Embed
from utils import *
from wolfram import AsyncApp


class Wolfram(Cog):
    def __init__(self, client):
        self.client = client
        self.data = return_config()

    @command(aliases=['wolfram', 'alpha', 'calc', 'calculate'], description='Send a request for example to calculate '
                                                                            'something with the Wolframalpha api')
    async def wolf(self, ctx):
        wait_embed = Embed(
            title='Wolfram ALPHA',
            color=colour()
        )
        wait_embed.description = 'Please type what you want to get from the api. ' \
                                 'Your request will be timed out in 5 minutes'
        sent_message = await ctx.send(embed=wait_embed)
        resp = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=600)
        app = AsyncApp(self.data['api_keys']['wolframalpha'])
        result = await app.short(str(resp.content))
        result = result.replace('{', '').replace('}', '').replace('->', ' = ')
        wait_embed.add_field(
            name='Input',
            value=resp.content, inline=False
        )
        wait_embed.add_field(
            name='Output',
            value=result, inline=False
        )
        await resp.delete()
        await sent_message.edit(embed=wait_embed)


def setup(client):
    client.add_cog(Wolfram(client))
