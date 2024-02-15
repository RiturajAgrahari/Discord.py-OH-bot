import os
import time
import random
import asyncio
import discord
import datetime

from typing import Optional, Literal
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

from database import (checking_main_profile, check_status, add_energy_link, update_status, reset_data, check_energy_link
, leaderboard_data, profile)
from embeds import daily_claim, help_embed, guess_embed, energy_link_leaderboard
from rock_paper_scissor import rps, RPS_stat, rps_leaderboard
from tic_tac_toe import tictactoe, ttt_stat, ttt_leaderboard
from guess_the_number import guess, guess_stat, gtn_leaderboard
from events import check_inventory, check_event_status, once_human_event

load_dotenv()

MAIN_GUILD_ID = int(os.getenv("MAIN_SERVER_ID"))

ENERGY_LINK = '<:energylinks:1146372968570691604>'


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        MAIN_GUILD = discord.Object(id=MAIN_GUILD_ID)
        self.tree.copy_global_to(guild=MAIN_GUILD)
        await self.tree.sync(guild=MAIN_GUILD)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await check_time.start()

@tasks.loop(minutes=1)
async def check_time():
    # Get the current UTC time
    current_time_utc = datetime.datetime.utcnow().time()

    # Check if it's UTC 00:00
    if current_time_utc.hour == 0 and current_time_utc.minute == 0:
        await daily_checkup()


@client.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.private:
        print(f'DM --> [{message.author}] : {message.content}')

    # Check if the message author is not client itself
    if message.author == client.user:
        pass

    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = message.guild.name
        # print(f'[{channel}]_____{username}_____: {user_message}')

    if message.content == '/hi':
        print('hi')

@client.tree.command(name="help", description="It will show you the list of commands available!")
async def helpdesk(interaction: discord.Interaction):
    avatar_url = await get_avatar(interaction)
    embed = await help_embed(interaction.user.name, avatar_url)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@client.tree.command(name="daily", description="Claim your daily energy link!")
async def daily(interaction: discord.Interaction):
    uid = await checking_main_profile(interaction)
    status = await check_status(uid)
    if status == 'not_claimed':
        coins = random.randint(50, 101)
        await add_energy_link(coins, uid)
        await update_status(uid)
        embed = await daily_claim(interaction, coins)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            f'{interaction.user.mention} You already claimed your today\'s daily energy link', ephemeral=True)


@client.tree.command(name="energy_link", description="energy links")
async def check(interaction: discord.Interaction):
    uid = await checking_main_profile(interaction)
    energy = await check_energy_link(uid)
    await interaction.response.send_message(f'You have {energy} <:energylinks:1146372968570691604>!', ephemeral=True)


@client.tree.command(name="play", description="Choose a game to play!")
async def play(interaction: discord.Interaction, games: Literal['rock paper scissor', 'guess the number', 'tic tac toe']):  #'tic tac toe', 'jumble words'
    if games == 'rock paper scissor':
        await rps(interaction)
    elif games == 'tic tac toe':
        await tictactoe(interaction)
    elif games == 'guess the number':
        embed = await guess_embed(interaction)
        await interaction.response.send_message(embed=embed)
        await guess(client, interaction)
    # elif games == 'jumble words':
    #     pass
    else:
        await send_error(__file__, '/play', 'user trying to play unknown game!')
        print(games)


@client.tree.command(name="statistics", description="Choose a game to check the statistics of a specific player!")
async def stat(interaction: discord.Interaction, games: Literal['rock paper scissor', 'guess the number', 'tic tac toe'],
               member: discord.Member = None):  # , 'jumble words'
    game = games
    avatar_url = await get_avatar(interaction)
    try:
        game = games.replace(' ', '_')
        avatar_url = member.avatar.url
    except Exception as e:
        print(e)
    finally:
        print(f'{interaction.user} checking {member} statistics in {games}')
        if games == 'rock paper scissor':
            if member is None:
                await RPS_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar_url)
            else:
                await RPS_stat(member.mention, games, game, interaction, member, avatar_url)
        elif games == 'guess the number':
            if member is None:
                await guess_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar_url)
            else:
                await guess_stat(member.mention, games, game, interaction, member, avatar_url)
        elif games == 'tic tac toe':
            if member is None:
                await ttt_stat(interaction.user.mention, games, game, interaction, interaction.user, avatar_url)
            else:
                await ttt_stat(member.mention, games, game, interaction, member, avatar_url)
        else:
            await send_error(__file__, '/statistics', 'user trying to check stat of unknown game!')
            print(games)


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
        status = await check_event_status(id)
        if status == 'Not Claimed':
            await once_human_event(id, interaction)
        else:
            await interaction.response.send_message(f'You already claimed the reward!\nThis is a one time event',
                                                    ephemeral=True)

# Last Optimization [19-01-2024]
async def get_avatar(interaction):
    try:
        avatar_url = interaction.user.avatar.url
        return avatar_url
    except Exception as e:
        default_avatar_url = 'https://cdn.discordapp.com/attachments/1171092440233541632/1207647618444820480/icon_new_256.png?ex=65e0687d&is=65cdf37d&hm=4c631bb83bba102d62d3648bc0493175dd9a627631368d29d49ec65cb2f21bdf&'
        return default_avatar_url

# Created at [19-01-2024] --> Need to be Tested
async def daily_checkup():
    try:
        await reset_data()
    except Exception as e:
        await send_error(__file__, 'daily_checkup()', e)


# Last Optimization [19-01-2024] --> Need Relocation
async def send_error(file, function_name, error, server='Once Human'):
    embed = discord.Embed(title=f'{server} Server',
        description=file,
        color=discord.Color.red()
    )
    embed.add_field(
        name=function_name,
        value=error,
        inline=False
    )
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)


@client.event
async def on_error(event, *args, **kwargs):
    try:
        message = args[0] # Gets the message object
        await send_error(__file__, event, 'Their is some error!')
    except Exception as e:
        print(e)


client.run(os.getenv("TOKEN"))