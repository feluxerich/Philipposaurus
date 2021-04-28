from discord.ext.commands import Cog, command
from discord import Embed
from requests import get
from utils import *
from json import dumps


class Osu(Cog):
    def __init__(self, client):
        self.client = client
        self.data = return_config()

    @command(description='With this command you can get the statistics of a osu player')
    async def osustats(self, ctx, player_name):
        osu_resp = get(f'https://osu.ppy.sh/api/get_user?u={player_name}&k={self.data["api_keys"]["osu"]}').json()[0]
        osu_stats_embed = Embed(
            title='Osu Stats',
            color=0x00ff00
        )
        osu_stats_embed.add_field(
            name='Playerdata',
            value=f'ID: {osu_resp["user_id"]}\nName: {osu_resp["username"]}',
            inline=True
        )
        osu_stats_embed.add_field(
            name='Points',
            value=f'300-Hits: {osu_resp["count300"]}\n100-Hits: {osu_resp["count100"]}\n'
                  f'50-Hits: {osu_resp["count50"]}',
            inline=True
        )
        osu_stats_embed.add_field(
            name='Plays',
            value=f'Plays: {osu_resp["playcount"]}\nSilver-SS: {osu_resp["count_rank_ssh"]}\n'
                  f'SS: {osu_resp["count_rank_ss"]}\nSilver-S: {osu_resp["count_rank_sh"]}\n'
                  f'S: {osu_resp["count_rank_s"]}\nA: {osu_resp["count_rank_a"]}\n'
                  f'Accuracy: {osu_resp["accuracy"]}',
            inline=False
        )
        osu_stats_embed.set_thumbnail(url=f'http://s.ppy.sh/a/{osu_resp["user_id"]}')
        await ctx.send(embed=osu_stats_embed)
        print(dumps(osu_resp, indent=4))


def setup(client):
    client.add_cog(Osu(client))
