import discord
import asyncio
from typing import Optional
from discord import app_commands
from typing import Literal
from rock_paper_scissor import *
from tic_tac_toe import *
from database import *
from embeds import *
import time
from guess_the_number import *
from events import check_inventory, once_human_event, check_status
import random

MY_GUILD = discord.Object(id='your_guild_id')


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.private:
        print(f"[{message.author}] : {message.content}")

    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        print(f'[{channel}]_____{username}_____: {user_message}')

    if message.author == client.user:
        pass

    elif message.content == '/hi':
        print('hi')

    elif message.content == 'setup' and message.author.mention == '<@568179896459722753>':
        print('setup successful')
        embed = await update_setup()
        await message.channel.send(embed=embed)


@client.tree.command(name="daily", description="Claim your daily energy link!")
async def daily(interaction: discord.Interaction):
    uid = await checking_main_profile(interaction)
    T = time.time()
    claimed_time = T // 1
    status, interval = await check_time(claimed_time, uid)
    if status is True:
        coins = random.randint(50, 101)
        await add_energy_link(uid, coins)
        await interaction.response.send_message(f'{interaction.user.mention} You got {coins}'
                                                f' <:energylinks:1146372968570691604>!', ephemeral=True)
    else:
        time_left = (24 * 60 * 60 - interval)
        hour = time_left // 3600
        minute = time_left % 3600 // 60
        second = time_left % 3600 % 60
        await interaction.response.send_message(
            f'{interaction.user.mention} You can claim your daily energy link after {int(hour)} hour'
            f' {int(minute)} minutes {int(second)} seconds!', ephemeral=True)


@client.tree.command(name="energy_link", description="energy links")
async def check(interaction: discord.Interaction):
    uid = await checking_main_profile(interaction)
    energy = await energy_link(uid)
    await interaction.response.send_message(f'You have {energy} <:energylinks:1146372968570691604>!', ephemeral=True)


@client.tree.command(name="help", description="It will show you the list of commands available!")
async def helpdesk(interaction: discord.Interaction):
    await checking_main_profile(interaction)
    embed = await help_embed(interaction)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.tree.command(name="play", description="Choose a game to play!")
async def play(interaction: discord.Interaction, games: Literal['rock paper scissor', 'guess the number', 'tic tac toe']):  #'tic tac toe', 'jumble words'
    print(games)
    if games == 'rock paper scissor':
        await rps(interaction)
    elif games == 'guess the number':
        embed = await guess_embed(interaction)
        await interaction.response.send_message(embed=embed)
        await guess(client, interaction)
    elif games == 'tic tac toe':
        await tictactoe(interaction)
    else:
        print('error in main.py client tree command!')
        

@client.tree.command(name="statistics", description="Choose a game to check the statistics of a specific player!")
async def stat(interaction: discord.Interaction, games: Literal['rock paper scissor', 'guess the number', 'tic tac toe'],
               member: discord.Member = None):  # , 'jumble words'
    game = games
    avatar = interaction.user.avatar.url
    try:
        game = games.replace(' ', '_')
        avatar = member.avatar.url
    except Exception as e:
        print(e)
    finally:
        print(f'{interaction.user} checking {member} statistics in {games}')
        if games == 'rock paper scissor':
            if member is None:
                await RPS_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar)
            else:
                await RPS_stat(member.mention, games, game, interaction, member, avatar)
        elif games == 'guess the number':
            if member is None:
                await guess_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar)
            else:
                await guess_stat(member.mention, games, game, interaction, member, avatar)
        elif games == 'tic tac toe':
            if member is None:
                await ttt_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar)
            else:
                await ttt_stat(member.mention, games, game, interaction, member, avatar)
        else:
            print('error in main.py client tree command!')


@client.tree.command(name="leaderboard", description="Which game leaderboard you want to check!")
async def leaderboard(interaction: discord.Interaction, games: Literal['rock paper scissor', 'guess the number',
                                                                       'tic tac toe', 'energy link']):
    if games == 'rock paper scissor':
        a = leaderboard_data('rock_paper_scissor')
        win_data = a.win_board()
        await rps_leaderboard(interaction, 'rock_paper_scissor', 'Rock Paper Scissor', 'Wins', win_data)
    elif games == 'guess the number':
        a = leaderboard_data('guess_the_number')
        win_data = a.win_board()
        await gtn_leaderboard(interaction, 'guess_the_number', 'Guess the Number', 'Wins', win_data)
    elif games == 'tic tac toe':
        a = leaderboard_data('tic_tac_toe')
        win_data = a.win_board()
        await ttt_leaderboard(interaction, 'tic_tac_toe', 'Tic Tac Toe', 'Wins', win_data)
    elif games == 'energy link':
        a = leaderboard_data('guess_the_number')
        data = a.energy_links()
        embed = await energy_link_leaderboard(interaction, data)
        await interaction.response.send_message(embed=embed)
    else:
        print('under development!')


@client.tree.command(name="inventory", description="Check out your inventory!")
async def inventory(interaction: discord.Interaction):
    id = await checking_main_profile(interaction)
    await check_inventory(id, interaction)


@client.tree.command(name="events", description="Cost - 100 Energy Links")
async def events(interaction: discord.Interaction, event: Literal["open letter box"]):
    if event == 'open letter box':
        a = profile(interaction.user.mention, 'discord_id')
        id = a.get_id()
        status = await check_status(id)
        if status == 'Not Claimed':
            await once_human_event(id, interaction)
        else:
            await interaction.response.send_message(f'You already claimed the reward!\nThis is a one time event',
                                                    ephemeral=True)


client.run('your_bot_token')