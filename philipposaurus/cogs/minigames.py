from discord.ext.commands import Cog, command
from discord import Embed, Member
from utils import *
from asyncio import TimeoutError


class Minigames(Cog):
    def __init__(self, client):
        self.client = client

    @command(aliases=['tictactoe'], description='Play tic-tac-toe against a user')
    async def ttt(self, ctx, member: Member):
        timeout_embed = Embed(
            title='Timeout',
            description='The match request timed out after 60 seconds or the request was denied',
            color=colour()
        )
        invite_embed = Embed(
            title='Tic Tac Toe',
            description=f'{ctx.author.mention} invited {member.mention} to play tic-tac-toe. Accept with 🟢 '
                        f'or deny with 🔴. This request will time out in 60 seconds',
            color=colour()
        )
        invite_sent = await ctx.send(embed=invite_embed)
        await invite_sent.add_reaction('🟢')
        await invite_sent.add_reaction('🔴')
        try:
            react, reaction_user = await self.client.wait_for(
                'reaction_add',
                check=lambda reaction, user: user == member,
                timeout=60
            )
            if str(react.emoji) == '🟢':
                fields = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                # Red 🔴
                # Green 🟢
                player1 = member
                player2 = ctx.author
                won = None
                player_turn = player1
                tic_tac_toe_embed = Embed(
                    title='Tic Tac Toe',
                    color=colour()
                )
                tic_tac_toe_embed.description = f'```\n' \
                                                f'+---+---+---+\n' \
                                                f'| {fields[0]} | {fields[1]} | {fields[2]} |\n' \
                                                f'+---+---+---+\n' \
                                                f'| {fields[3]} | {fields[4]} | {fields[5]} |\n' \
                                                f'+---+---+---+\n' \
                                                f'| {fields[6]} | {fields[7]} | {fields[8]} |\n' \
                                                f'+---+---+---+\n' \
                                                f'```'
                sent = await ctx.send(embed=tic_tac_toe_embed)
                while won is None:
                    response = await self.client.wait_for('message', check=lambda msg: msg.author == player_turn)
                    if response.content.isdigit() and int(response.content) <= 9 and str(response.content) in fields:
                        if player_turn == player1:
                            fields[int(response.content) - 1] = 'X'
                            player_turn = player2
                        elif player_turn == player2:
                            fields[int(response.content) - 1] = '0'
                            player_turn = player1
                    else:
                        invalid_input_embed = Embed(
                            title='Tic Tac Toe',
                            description='Invalid input. Please type a valid number',
                            color=colour()
                        )
                        await ctx.send(embed=invalid_input_embed, delete_after=10)
                    await response.delete()
                    if fields[0] == fields[1] and fields[0] == fields[2] and fields[0] == 'X' or \
                            fields[3] == fields[4] and fields[3] == fields[5] and fields[3] == 'X' or \
                            fields[6] == fields[7] and fields[6] == fields[8] and fields[6] == 'X' or \
                            fields[0] == fields[3] and fields[0] == fields[6] and fields[0] == 'X' or \
                            fields[1] == fields[4] and fields[1] == fields[7] and fields[1] == 'X' or \
                            fields[2] == fields[5] and fields[2] == fields[8] and fields[2] == 'X' or \
                            fields[0] == fields[4] and fields[0] == fields[8] and fields[0] == 'X' or \
                            fields[2] == fields[4] and fields[2] == fields[6] and fields[2] == 'X':
                        won = player1
                        continue
                    if fields[0] == fields[1] and fields[0] == fields[2] and fields[0] == '0' or \
                            fields[3] == fields[4] and fields[3] == fields[5] and fields[3] == '0' or \
                            fields[6] == fields[7] and fields[6] == fields[8] and fields[6] == '0' or \
                            fields[0] == fields[3] and fields[0] == fields[6] and fields[0] == '0' or \
                            fields[1] == fields[4] and fields[1] == fields[7] and fields[1] == '0' or \
                            fields[2] == fields[5] and fields[2] == fields[8] and fields[2] == '0' or \
                            fields[0] == fields[4] and fields[0] == fields[8] and fields[0] == '0' or \
                            fields[2] == fields[4] and fields[2] == fields[6] and fields[2] == '0':
                        won = player2
                        continue
                    if is_num(fields) is False:
                        won = False
                    tic_tac_toe_embed.description = f'```\n' \
                                                    f'+---+---+---+\n' \
                                                    f'| {fields[0]} | {fields[1]} | {fields[2]} |\n' \
                                                    f'+---+---+---+\n' \
                                                    f'| {fields[3]} | {fields[4]} | {fields[5]} |\n' \
                                                    f'+---+---+---+\n' \
                                                    f'| {fields[6]} | {fields[7]} | {fields[8]} |\n' \
                                                    f'+---+---+---+\n' \
                                                    f'```'
                    await sent.edit(embed=tic_tac_toe_embed)
                if won:
                    tic_tac_toe_embed.description = f'{won.mention} won the game'
                    await sent.edit(embed=tic_tac_toe_embed)
                elif won is False:
                    tic_tac_toe_embed.description = 'Draw'
                    await sent.edit(embed=tic_tac_toe_embed)
            else:
                await ctx.send(embed=timeout_embed)
        except TimeoutError:
            await ctx.send(embed=timeout_embed)


def setup(client):
    client.add_cog(Minigames(client))
