from discord.ext.commands import Cog, command
from discord import Embed, Member
from requests import get
from base64 import b64decode
from utils import *
from aiohttp import ClientSession


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
                color=colour()
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
            guild_params = {
                "key": str(api_key),
                "player": uuid['id']
            }
            try:
                player = get('https://api.hypixel.net/player', params=params).json()
                status = get('https://api.hypixel.net/status', params=params).json()
                recent = get('https://api.hypixel.net/recentgames', params=params).json()['games'][0]['gameType']
                guild = get('https://api.hypixel.net/guild', params=guild_params).json()
                achievement = player['player']['achievementsOneTime'][-1].replace('_', ' ').capitalize()
                hypixel_stats_embed = Embed(
                    title='HyPixel',
                    color=colour()
                )
                hypixel_stats_embed.add_field(
                    name='Last Advancements', value=achievement, inline=True
                )
                try:
                    rank = player['player']['newPackageRank']
                    rank = rank.replace('_', ' ')
                    hypixel_stats_embed.add_field(
                        name='Rank',
                        value=rank, inline=True
                    )
                except KeyError:
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
                hypixel_stats_embed.add_field(
                    name='Recently Played',
                    value=recent.capitalize(), inline=True
                )
                try:
                    hypixel_stats_embed.add_field(
                        name='Guild',
                        value=guild['guild']['name']
                    )
                except TypeError:
                    pass
                hypixel_stats_embed.set_thumbnail(url=f'https://mc-heads.net/avatar/{uuid["id"]}')
                await ctx.send(embed=hypixel_stats_embed)
            except Exception as e:
                raise e

    @command(description='Gives the name history of an specific user')
    async def name_history(self, ctx, *, mc_name):
        uuid = get(f'https://api.mojang.com/users/profiles/minecraft/{mc_name}').json()
        if uuid:
            user = get(f'https://api.mojang.com/user/profiles/{uuid["id"]}/names').json()
            names = ''
            for name in user:
                if 'changedToAt' not in name:
                    names += f'**{name["name"]}** - created\n'
                    continue
                names += f'**{name["name"]}**\n'
            name_history_embed = Embed(
                title='Minecraft Name History',
                description=names,
                color=colour()
            )
            await ctx.send(embed=name_history_embed)

    @command(description='Get the minecraft account of a discord account if this user linked his account with the bot')
    async def get_minecraft(self, ctx, member: Member):
        url = f'{self.data["api_keys"]["bridge_api"]}/accounts/discord/{int(member.id)}'
        async with ClientSession() as session:
            async with await session.get(url) as response:
                output = await response.json()
        get_minecraft_embed = Embed(
            title='Bridge api',
            color=colour()
        )
        get_minecraft_embed.add_field(
            name='Discord',
            value=f'ID: {output["discord"]["id"]}\nName: {output["discord"]["name"]}',
            inline=True
        )
        get_minecraft_embed.add_field(
            name='Minecraft',
            value=f'ID: {output["minecraft"]["id"]}\nName: {output["minecraft"]["name"]}',
            inline=True
        )
        get_minecraft_embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=get_minecraft_embed)

    # @command(description='Link your minecraft account with your discord account')
    # async def link_minecraft(self, ctx, *, mc_name):
    #     url = f'{self.data["api_keys"]["bridge_api"]}/accounts'
    #     uuid = f'https://api.mojang.com/users/profiles/minecraft/{mc_name}'
    #     async with ClientSession() as session:
    #         async with await session.get(uuid) as uuid_resp:
    #             uuid_resp = await uuid_resp.json()
    #             data = {
    #                 "discord_id": str(ctx.author.id),
    #                 "discord_name": str(ctx.author.name),
    #                 "minecraft_id": str(uuid_resp["id"]),
    #                 "minecraft_name": str(uuid_resp["name"])
    #             }
    #         async with await session.post(url, json=data) as response:
    #             output = await response.json()
    #     get_minecraft_embed = Embed(
    #         title='Bridge api',
    #         color=colour()
    #     )
    #     get_minecraft_embed.add_field(
    #         name='Response',
    #         value=str(output['message'])
    #     )
    #     await ctx.send(embed=get_minecraft_embed)


def setup(client):
    client.add_cog(Minecraft(client))
