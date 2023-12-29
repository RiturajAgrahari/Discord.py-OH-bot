import mysql.connector
import discord
from discord.ui import Button, View
from embeds import *
from database import profile, leaderboard_data, checking_main_profile, all_game_profile
import inspect


async def open_database():
    mydb = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    return mydb

Player = []
player_name = []
pl_id = []
uid_data = []
List = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


async def clear_data():
    pl_id.clear()
    Player.clear()
    player_name.clear()
    uid_data.clear()
    List.clear()
    for i in range(0, 10):
        List.append(i)


async def tictactoe(interaction):
    await clear_data()

    embed = await tic_tac_toe_embed(interaction)

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='Join', style=discord.ButtonStyle.blurple, custom_id="my_button")
        async def ttt(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.click_count == 0:
                self.click_count += 1
                uid = await checking_main_profile(interaction)
                uid_data.append(uid)
                client1 = str(interaction.user)
                print(f'{client1} joined as a player 1')
                await interaction.response.send_message(f'{interaction.user.mention} Joined!', ephemeral=True)
                player_name.append(client1)
                pl_id.append(interaction.user.mention)
                Player.append(client1.split('#')[0])

            elif self.click_count == 1 and str(interaction.user.mention) not in pl_id:
                self.click_count += 1
                uid = await checking_main_profile(interaction)
                uid_data.append(uid)
                client2 = str(interaction.user)
                print(f'{client2} joined as a player 2')
                player_name.append(client2)
                Player.append(client2.split('#')[0])
                pl_id.append(interaction.user.mention)
                button.disabled = True
                await interaction.response.edit_message(view=self)
                await interaction.followup.send(f'Match is started!\n{pl_id[0]} V/S {pl_id[1]}')
                await game(interaction, Player[0], Player[1])
                print(f'Joined player --> {player_name} ')
            else:
                if interaction.user.mention in pl_id:
                    await interaction.response.send_message(f'You already joined the match!', ephemeral=True)
                else:
                    await interaction.response.send_message(f'Match Ended!', ephemeral=True)

    view = MyView()
    view.response = await interaction.response.send_message(embed=embed, view=view)


async def game(interaction, player1, player2):
    embed = await ttt_game_embed(player1, player2)

    class YourView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a11(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 0
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a12(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 1
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a13(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 2
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a21(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 3
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a22(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 4
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a23(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 5
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a31(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 6
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a32(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 7
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a33(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 8
            await move(self, interaction, button, value)

    view = YourView()
    view.response = await interaction.followup.send(embed=embed, view=view)


async def move(self, interaction, button, given):
    try:
        if self.click_count == 8:
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "cross"
            await results(interaction, given, player_move, None)
            if len(pl_id) == 0:
                print("someone won!")
            else:
                await interaction.followup.send(f"{pl_id[0]} and {pl_id[1]} it's a tie")
                await all_game_profile('tic_tac_toe', uid_data, ["tie", "tie"])
                # await checking_profile(Player, pl_id, ["tie", "tie"])

        elif self.click_count % 2 == 0 and str(interaction.user.mention) == pl_id[0]:
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "cross"
            await results(interaction, given, player_move, pl_id[1])
        elif self.click_count % 2 != 0 and str(interaction.user) == player_name[1]:
            print(interaction.user)
            button.label = '⭕'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "circle"
            await results(interaction, given, player_move, pl_id[0])
            print(self.click_count)
        else:
            if interaction.user.mention in pl_id:
                await interaction.response.send_message(f'This is not your turn!', ephemeral=True)
            else:
                await interaction.response.send_message(f'Either you did not joined the game or the game is already'
                                                        f' ended!', ephemeral=True)
    except Exception as e:
        print(e)


async def results(interaction, value, player_move, turn):
    print(value)
    List.insert(value, player_move)
    List.remove(value)
    print(List)
    if List[0] == List[3] == List[6]:
        position = 0
        await winner(interaction, position)
    elif List[1] == List[4] == List[7]:
        position = 1
        await winner(interaction, position)
    elif List[2] == List[5] == List[8]:
        position = 2
        await winner(interaction, position)
    elif List[0] == List[1] == List[2]:
        position = 0
        await winner(interaction, position)
    elif List[3] == List[4] == List[5]:
        position = 3
        await winner(interaction, position)
    elif List[6] == List[7] == List[8]:
        position = 6
        await winner(interaction, position)
    elif List[0] == List[4] == List[8]:
        position = 0
        await winner(interaction, position)
    elif List[2] == List[4] == List[6]:
        position = 2
        await winner(interaction, position)
    else:
        pass


async def winner(interaction, position):
    await interaction.followup.send(f'{interaction.user.mention} you won!<:H37sneer:997036721843736637>')
    if List[position] == "cross":
        await all_game_profile('tic_tac_toe', uid_data, ["wins", "loss"])
    else:
        await all_game_profile('tic_tac_toe', uid_data, ["loss", "wins"])
    await clear_data()


async def get_ttt_data(id, game):
    mydb = await open_database()
    mycursor = mydb.cursor()
    sql = f'select * from {game} where id = {id}'
    mycursor.execute(sql)
    value = mycursor.fetchall()[0]
    mydb.close()
    return value[1], value[2], value[3]


async def ttt_stat(discord_id, games, game, interaction, name, avatar):
    try:
        a = profile(discord_id, 'discord_id')
        id = a.get_id()
        Win, Loss, Tie = await get_ttt_data(id, game)
        embed = await ttt_stat_embed(games, name, Win, Loss, Tie, avatar, interaction)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f'No profile exist with this name.', ephemeral=True)


async def ttt_leaderboard(interaction, game, game_name, default, data):
    embed = discord.Embed(
        title=f'{default} Leaderboard',
        description=f'**{game_name}**',
        color=discord.Color.red()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png')
    # length = len(data) if len(data) < 10 else 10
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
                # await interaction.message.delete()
                data = leaderboard_data(game)
                await ttt_leaderboard(interaction, 'tic_tac_toe', 'Tic Tac Toe', 'Wins', data.win_board())
        else:
            @discord.ui.button(label='Wins', style=discord.ButtonStyle.green, disabled=True)
            async def win(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Loss':
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=False)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                # await interaction.message.delete()
                data = leaderboard_data(game)
                await ttt_leaderboard(interaction, 'tic_tac_toe', 'Tic Tac Toe', 'Loss', data.loss_board())
        else:
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=True)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Win Rate':
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=False)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                # await interaction.message.delete()
                data = leaderboard_data(game)
                await ttt_leaderboard(interaction, 'tic_tac_toe', 'Tic Tac Toe', 'Win Rate', data.win_rate())
        else:
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=True)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Tie':
            @discord.ui.button(label='Tie', style=discord.ButtonStyle.gray, disabled=False)
            async def tie(self, interaction: discord.Interaction, button: discord.ui.Button):
                # await interaction.message.delete()
                data = leaderboard_data(game)
                await ttt_leaderboard(interaction, 'tic_tac_toe', 'Tic Tac Toe', 'Tie', data.tie_board())
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
