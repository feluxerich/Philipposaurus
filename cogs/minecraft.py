from discord.ext.commands import Cog, command
from discord import Embed
from requests import get
from base64 import b64decode
from utils import *


class Minecraft(Cog):
    def __init__(self, client):
        self.client = client
        self.data = return_config()

    @command(description='Grab a skin from a minecraft user. This commands sends then an embed with a picture and'
                         'the link to the skin')
    async def grab(self, ctx, *, mc_name):
        uuid = get(f'https://api.mojang.com/users/profiles/minecraft/{mc_name}').json()
        if uuid:
            user = get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid["id"]}').json()
            skin = str(b64decode(user['properties'][0]['value'])).split('"')[17]
            skin_grab_embed = Embed(
                title='Skin-Grabber',
                description=f'[The Skin]({skin})',
                color=0x00ff00
            )
            skin_grab_embed.set_image(url=str(skin))
            await ctx.send(embed=skin_grab_embed)

    @command(description='This commands returns the stats of an user on hypixel')
    async def hypixel(self, ctx, *, mc_name):
        uuid = get(f'https://api.mojang.com/users/profiles/minecraft/{mc_name}').json()
        api_key = self.data['api_keys']['hypixel']
        if uuid:
            params = {
                "key": str(api_key),
                "uuid": uuid['id']
            }

            player = get('https://api.hypixel.net/player', params=params).json()
            status = get('https://api.hypixel.net/status', params=params).json()
            hypixel_stats_embed = Embed(
                title='HyPixel',
                color=0x00ff00
            )
            advancements = ""
            for advancement in player['player']['achievementsOneTime'][-5:]:
                advancements += f'{advancement.replace("_", " ").capitalize()}\n'
            hypixel_stats_embed.add_field(
                name='Last Advancements', value=advancements, inline=True
            )
            try:
                rank = player['player']['newPackageRank']
                rank = rank.replace('_', ' ')
                hypixel_stats_embed.add_field(
                    name='Rank',
                    value=rank, inline=True
                )
            except:
                pass
            hypixel_stats_embed.add_field(
                name='Most Played',
                value=player['player']['mostRecentGameType'].capitalize(), inline=True
            )
            if status['session']['online'] is True:
                online = '🟢 Online'
            else:
                online = '🔴 Offline'
            hypixel_stats_embed.add_field(
                name='Status',
                value=online, inline=True
            )
            hypixel_stats_embed.set_thumbnail(url=f'https://mc-heads.net/avatar/{uuid["id"]}')
            await ctx.send(embed=hypixel_stats_embed)


def setup(client):
    client.add_cog(Minecraft(client))
