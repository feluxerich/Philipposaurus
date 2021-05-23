from discord.ext.commands import Cog, command
from discord import Embed, Member
from requests import get
from asyncio import sleep
from utils import colour


class Joke(Cog):
    def __init__(self, client):
        self.client = client

    @command(description='Sends a random Joke. After ten seconds there will appear the pointe')
    async def joke(self, ctx):
        joke_embed = Embed(
            title='Joke',
            color=colour()
        )
        joke = get('https://official-joke-api.appspot.com/jokes/random').json()
        joke_embed.description = joke['setup']
        sent_message = await ctx.send(embed=joke_embed)
        await sleep(10)
        joke_embed.description = joke['punchline']
        await sent_message.edit(embed=joke_embed, delete_after=10)

    @command(aliases=['rename', 'nickname'], description='Change the nickname of a user to a very funny nickname')
    async def nick(self, ctx, member: Member, *, nickname):
        if len(nickname) <= 32:
            await member.edit(nick=nickname)
            changed_embed = Embed(
                title='Nickname',
                description=f'The nickname was changed successfully to {nickname}',
                colour=colour()
            )
            await ctx.send(embed=changed_embed)
        else:
            too_long_embed = Embed(
                title='Nickname',
                description='The length of the nickname must be fewer than 32',
                colour=colour()
            )
            await ctx.send(embed=too_long_embed)


def setup(client):
    client.add_cog(Joke(client))
