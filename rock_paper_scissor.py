import mysql.connector
import discord
import os
from discord.ui import Button, View
from embeds import *
from database import profile, leaderboard_data, checking_main_profile, all_game_profile, select_query
import inspect
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MY_SQL_HOST")
USER = os.getenv("MY_SQL_USER")
PASSWORD = os.getenv("MY_SQL_PASSWORD")
DATABASE = os.getenv("MY_SQL_DATABASE")

discord_id_data = []
moves_data = []
username_data = []
uid_data = []


async def open_database():
    mydb = mysql.connector.connect(
      host=HOST,
      user=USER,
      password=PASSWORD,
      database=DATABASE
    )
    return mydb

async def rps(interaction):
    discord_id_data.clear()
    moves_data.clear()
    username_data.clear()
    uid_data.clear()
    embed = await rock_paper_scissors_embed(interaction)

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='Rock ✊', style=discord.ButtonStyle.blurple)
        async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
            await fun(self, interaction, 'rock')

        @discord.ui.button(label='Paper ✋', style=discord.ButtonStyle.green)
        async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
            await fun(self, interaction, 'paper')

        @discord.ui.button(label='Scissors ✌️', style=discord.ButtonStyle.red)
        async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
            await fun(self, interaction, 'scissors')

    view = MyView()
    view.response = await interaction.response.send_message(embed=embed, view=view)


async def fun(self, interaction, player_move):
    if self.click_count == 0 and not interaction.user.mention in discord_id_data:
        self.click_count += 1
        uid = await checking_main_profile(interaction)
        uid_data.append(uid)
        discord_id_data.append(interaction.user.mention)
        await interaction.response.send_message(f'{interaction.user.mention} selected his move :man_tipping_hand:', ephemeral=False)
        self.value = True
        username_data.append(str(interaction.user).split('#')[0] )
        moves_data.append(player_move)

    elif self.click_count == 1 and not interaction.user.mention in discord_id_data:
        self.click_count += 1
        uid = await checking_main_profile(interaction)
        uid_data.append(uid)
        discord_id_data.append(interaction.user.mention)
        await interaction.response.send_message(f'{interaction.user.mention} selected his move :man_tipping_hand:', ephemeral=False)
        self.value = True
        username_data.append(str(interaction.user).split("#")[0])
        moves_data.append(player_move)

        if moves_data[0] == moves_data[1]:
            await interaction.followup.send(content=f"{discord_id_data[0]} selected {moves_data[0]}\n"
                                                    f"{discord_id_data[1]} selected {moves_data[1]}\n"
                                                    f"It's a Tie")
            await results(uid_data, ["tie", "tie"])

        else:
            if moves_data[0] == 'rock' and moves_data[1] == 'paper':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[1]} win.🥳')
                await results(uid_data, ["loss", "wins"])

            elif moves_data[0] == 'rock' and moves_data[1] == 'scissors':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[0]} win.🥳')
                await results(uid_data, ["wins", "loss"])

            elif moves_data[0] == 'paper' and moves_data[1] == 'rock':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[0]} win.🥳')
                await results(uid_data, ["wins", "loss"])

            elif moves_data[0] == 'paper' and moves_data[1] == 'scissors':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[1]} win.🥳')
                await results(uid_data, ["loss", "wins"])

            elif moves_data[0] == 'scissors' and moves_data[1] == 'rock':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[1]} win.🥳')
                await results(uid_data, ["loss", "wins"])

            elif moves_data[0] == 'scissors' and moves_data[1] == 'paper':
                await interaction.followup.send(content=f'{discord_id_data[0]} selected {moves_data[0]}\n{discord_id_data[1]} selected {moves_data[1]}\n{discord_id_data[0]} win.🥳')
                await results(uid_data, ["wins", "loss"])

            else:
                print('not possible in rps')
                print(discord_id_data)
                print(moves_data)
                print(username_data)
                print(uid_data)

    else:
        if interaction.user.mention in discord_id_data:
            await interaction.response.send_message(f'You have already choose your move', ephemeral=True)
        else:
            await interaction.response.send_message(f'The game is already ended use </play:1123130558768238665> again to play!',
                                                    ephemeral=True)


async def results(uid_data, pl_stat):
    await all_game_profile('rock_paper_scissor', uid_data, pl_stat)


async def get_rps_data(id, game):
    value = await select_query(column='*', table=game, condition_column='id', condition_value=id)
    return value[0][1], value[0][2], value[0][3]


async def RPS_stat(discord_id, games, game, interaction, name, avatar):
    try:
        a = profile(discord_id, 'discord_id')
        id = a.get_id()
        Win, Loss, Tie = await get_rps_data(id, game)
        embed = await rps_stat_embed(games, name, Win, Loss, Tie, avatar, interaction)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f'No profile exist with this name.', ephemeral=True)


async def rps_leaderboard(interaction, game, game_name, default, data):
    embed = discord.Embed(
        title=f'{default} Leaderboard',
        description=f'**{game_name}**',
        color=discord.Color.red()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png')
    for i in range(0, len(data)):
        if i < 3:
            top = [':first_place:', ':second_place:', ':third_place:']
            player = profile(data[i][0], 'id')
            embed.add_field(
                name=f'{top[i]} {player.get_name()}',
                value=f'{data[i][1]} {default}',
                inline=False
            )
        else:
            player = profile(data[i][0], 'id')
            embed.add_field(
                name=f'**#{i + 1}** {player.get_name()}',
                value=f'{data[i][1]} {default}',
                inline=False
            )
    embed.set_footer(text=f'Requested By: {interaction.user.name}')

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        if default != 'Wins':
            @discord.ui.button(label='Wins', style=discord.ButtonStyle.green, disabled=False)
            async def win(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await rps_leaderboard(interaction, 'rock_paper_scissor', 'Rock Paper Scissor', 'Wins', data.win_board())
        else:
            @discord.ui.button(label='Wins', style=discord.ButtonStyle.green, disabled=True)
            async def win(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Loss':
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=False)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await rps_leaderboard(interaction, 'rock_paper_scissor', 'Rock Paper Scissor', 'Loss', data.loss_board())
        else:
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=True)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Win Rate':
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=False)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await rps_leaderboard(interaction, 'rock_paper_scissor', 'Rock Paper Scissor', 'Win Rate', data.win_rate())
        else:
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=True)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Tie':
            @discord.ui.button(label='Tie', style=discord.ButtonStyle.gray, disabled=False)
            async def tie(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await rps_leaderboard(interaction, 'rock_paper_scissor', 'Rock Paper Scissor', 'Tie', data.tie_board())
        else:
            @discord.ui.button(label='Tie', style=discord.ButtonStyle.gray, disabled=True)
            async def tie(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

    view = MyView()
    caller_frame = inspect.stack()[1]
    caller_function = str(caller_frame.function)
    if caller_function == 'leaderboard':
        view.response = await interaction.response.send_message(embed=embed, view=view)
    else:
        view.response = await interaction.response.edit_message(embed=embed, view=view)




