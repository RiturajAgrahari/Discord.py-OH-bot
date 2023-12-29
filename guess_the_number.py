import discord
import random
import asyncio
import mysql.connector
from embeds import *
from database import profile, leaderboard_data, all_game_profile, checking_main_profile
import inspect


async def open_database():
    mydb = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    return mydb

uid_data = []


async def guess(client, interaction):
    uid_data.clear()
    uid = await checking_main_profile(interaction)
    uid_data.append(uid)
    answer = random.randint(1, 100)
    print(answer)
    tries = 0
    while True:
        if tries != 5:
            try:
                guess = await client.wait_for('message', timeout=60.0)
                if str(guess.author).split('#')[0] == str(interaction.user.name) and guess.content.isdigit():
                    # await guess.delete()
                    tries += 1
                    number = int(guess.content)
                    if number < answer:
                        if number < answer - 10:
                            await interaction.followup.send(f"{guess.author.mention}\nToo low! {5 - tries} tries left")
                        else:
                            await interaction.followup.send(f"{guess.author.mention}\nQuite low! {5 - tries} tries left")
                    elif number > answer:
                        if number > answer + 10:
                            await interaction.followup.send(f"{guess.author.mention}\nToo high! {5 - tries} tries left")
                        else:
                            await interaction.followup.send(f"{guess.author.mention}\nQuite high! {5 - tries} tries left")
                    else:
                        await interaction.followup.send(f"{guess.author.mention}\nYou guessed the correct number in"
                                                        f" {tries} tries!")
                        await results(uid_data, ['wins'])
                        break
                else:
                    pass
            except asyncio.TimeoutError:
                await interaction.followup.send(f"{interaction.user.mention} you didn't replied for a long time!"
                                                f"\nYou Lost", ephemeral=False)
                await results(uid_data, ['loss'])
                break
        else:
            await interaction.followup.send(f'{interaction.user.mention}\nYou lost, the correct number was : {answer}'
                                            , ephemeral=False)
            await results(uid_data, ['loss'])
            break


async def results(uid_data, pl_stat):
    await all_game_profile('guess_the_number', uid_data, pl_stat)


async def guess_stat(discord_id, games, game, interaction, name, avatar):
    print('phase 1 succesfull')
    try:
        a = profile(discord_id, 'discord_id')
        id = a.get_id()
        # id = await id_check(discord_id)
        Win, Loss = await get_guess_data(id, game)
        print('phase 2 succesfull')
        embed = await guess_stat_embed(games, name, Win, Loss, avatar, interaction)
        print('phase 3 succesfull')
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f'No profile exist with this name.', ephemeral=True)


async def get_guess_data(id, game):
    mydb = await open_database()
    mycursor = mydb.cursor()
    sql = f'select * from {game} where id = {id}'
    mycursor.execute(sql)
    value = mycursor.fetchall()[0]
    mydb.close()
    return value[1], value[2]


async def gtn_leaderboard(interaction, game, game_name, default, data):
    embed = discord.Embed(
        title=f'{default} Leaderboard',
        description=f'**{game_name}**',
        color=discord.Color.red()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png')
    # length = len(data) if len(data) < 10 else 10
    # print(length)
    for i in range(0, len(data)):
        if i < 3:
            top = [':first_place:', ':second_place:', ':third_place:']
            print(data)
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

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        if default != 'Wins':
            @discord.ui.button(label='Wins', style=discord.ButtonStyle.green, disabled=False)
            async def win(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await gtn_leaderboard(interaction, 'guess_the_number', 'Guess the Number', 'Wins', data.win_board())
        else:
            @discord.ui.button(label='Wins', style=discord.ButtonStyle.green, disabled=True)
            async def win(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Loss':
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=False)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await gtn_leaderboard(interaction, 'guess_the_number', 'Guess the Number', 'Loss', data.loss_board())
        else:
            @discord.ui.button(label='Loss', style=discord.ButtonStyle.red, disabled=True)
            async def loss(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

        if default != 'Win Rate':
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=False)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                data = leaderboard_data(game)
                await gtn_leaderboard(interaction, 'guess_the_number', 'Guess the Number', 'Win Rate', data.win_rate2())
        else:
            @discord.ui.button(label='Win Rate', style=discord.ButtonStyle.blurple, disabled=True)
            async def win_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
                print('error')

    view = MyView()
    caller_frame = inspect.stack()[1]
    caller_function = str(caller_frame.function)
    if caller_function == 'leaderboard':
        view.response = await interaction.response.send_message(embed=embed, view=view)
    else:
        view.response = await interaction.response.edit_message(embed=embed, view=view)