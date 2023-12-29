import discord
import string
from database import profile

alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']


async def help_embed(interaction):
    embed = discord.Embed(
        title='HELP-DESK',
        description='Here is the list of commands that is provided by the vultures bot!',
        color=discord.Color.green()
    )
    embed.add_field(
        name='/daily',
        value='To claim your daily energy link <:energylinks:1146372968570691604>',
        inline=False
    )
    embed.add_field(
        name='/energy_link',
        value='To check the number of energy links you have!',
        inline=False
    )
    embed.add_field(
        name='/play',
        value='To play games!',
        inline=False
    )
    embed.add_field(
        name='/statistics',
        value='To check statistics of a specific player!',
        inline=False
    )
    embed.add_field(
        name='/leaderboard',
        value='To check the game leaderboard of a players!',
        inline=False
    )
    embed.add_field(
        name='/event',
        value="To participate and play in events",
        inline=False
    )
    embed.add_field(
        name='/inventory',
        value="To check whats is in your inventory",
        inline=False
    )
    embed.set_image(url='https://cdn.discordapp.com/attachments/1107516904832245820/1155774955800236062/image.png')
    embed.set_footer(text=f'Requested By : {interaction.user.name}')
    return embed


async def rock_paper_scissors_embed(interaction):
    embed = discord.Embed(
        title="Rock_Paper_Scissors",
        description=f"Rock can destroy scissors by his strength ✊\n"
                    f"Scissors can cut paper by his sharpness ✌️\n"
                    f"Paper can wrap rock by his area ✋\n",
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Requested by : {interaction.user}")
    return embed


async def guess_embed(interaction):
    embed = discord.Embed(title=f'Guess the number',
                          description=f'In this game you have to guess the correct number between 1 and 100'
                                      f' within 5 tries!',
                          color=discord.Color.dark_gray())
    embed.set_footer(text=f'By {interaction.user}')
    return embed


async def rps_stat_embed(games, player_name, Win, Loss, Tie, avatar, interaction):
    Win_rate = Win / (Win + Loss + Tie)
    game = str(games).capitalize()
    embed = discord.Embed(
        title=game,
        color=discord.Color.green(),
    )
    embed.set_author(name=player_name, url=None, icon_url=avatar)
    embed.add_field(
        name='Wins',
        value=Win,
        inline=True
    )
    embed.add_field(
        name='Loss',
        value=Loss,
        inline=True
    )
    embed.add_field(
        name='Tie',
        value=Tie,
        inline=True
    )
    embed.add_field(
        name='Win Rate',
        value=Win_rate,
        inline=True
    )
    embed.set_footer(text=f'Requested By : {interaction.user.name}')
    return embed


async def guess_stat_embed(games, player_name, Win, Loss, avatar, interaction):
    Win_rate = Win / (Win + Loss)
    game = str(games).capitalize()
    embed = discord.Embed(title=game,
                          color=discord.Color.green())
    embed.set_author(name=player_name, url=None, icon_url=avatar)
    embed.add_field(name=f'Wins',
                    value=Win,
                    inline=True)
    embed.add_field(name=f'Loss',
                    value=Loss,
                    inline=True)
    embed.add_field(name=f'Win Rate',
                    value=Win_rate,
                    inline=False)
    embed.set_footer(text=f'Requested By : {interaction.user.name}')
    return embed


async def tic_tac_toe_embed(interaction):
    embed = discord.Embed(
        title="❌Tic_Tac_Toe❌",
        description=f"a game in which two players seek in alternate turns to complete a row, a column, or a diagonal"
                    f" with either three O's or three X's drawn in the spaces of a grid of nine squares.",
        color=discord.Color.green(),
    )

    embed.add_field(name="⭕Tap JOIN to get into the game⭕",
                    value="2 Players required",
                    inline=False)

    embed.set_footer(text=f"Requested By {interaction.user}")
    return embed


async def ttt_game_embed(player1, player2):
    embed = discord.Embed(title='Tic Tac Toe',
                          description='You have to complete a row,\n column, or a diagonal with your\n mark to win',
                          colour=discord.Colour.red())
    embed.add_field(name='Players Joined',
                    value=f'{player1} is ❌\n'
                          f'{player2} is ⭕',
                    inline=True)

    return embed


async def ttt_stat_embed(games, player_name, Win, Loss, Tie, avatar, interaction):
    Win_rate = Win / (Win + Loss + Tie)
    game = str(games).capitalize()
    embed = discord.Embed(
        title=game,
        color=discord.Color.green(),
    )
    embed.set_author(name=player_name, url=None, icon_url=avatar)
    embed.add_field(
        name='Wins',
        value=Win,
        inline=True
    )
    embed.add_field(
        name='Loss',
        value=Loss,
        inline=True
    )
    embed.add_field(
        name='Tie',
        value=Tie,
        inline=True
    )
    embed.add_field(
        name='Win Rate',
        value=Win_rate,
        inline=True
    )
    embed.set_footer(text=f'Requested By : {interaction.user.name}')
    return embed


async def energy_link_leaderboard(interaction, data):
    embed = discord.Embed(
        title=f'Energy links Leaderboard',
        description=f'Top 10 energy link holders',
        color=discord.Color.green()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png')
    # length = len(data) if len(data) < 10 else 10
    for i in range(0, len(data)):
        if i < 3:
            top = [':first_place:', ':second_place:', ':third_place:']
            player = profile(data[i][0], 'id')
            embed.add_field(
                name=f'{top[i]} {player.get_name()}',
                value=f'{data[i][1]} energy links',
                inline=False
            )
        else:
            player = profile(data[i][0], 'id')
            embed.add_field(
                name=f'**#{i + 1}** {player.get_name()}',
                value=f'{data[i][1]} energy links',
                inline=False
            )
    embed.set_footer(text=f'Requested By: {interaction.user.name}')
    return embed


async def letter_event(interaction, letter, owned):
    refund = 0
    reword = False
    win = False

    WORD = 'ONCE HUMAN'
    progress = {}
    new_word = WORD.replace(' ', '')
    for i in range(0, len(new_word)):  # {0: 'O', 1: 'N', 2: 'C', 3: 'E', 4: 'H', 5: 'U', 6: 'M', 7: 'A', 8: 'N'}
        progress[i] = new_word[i]

    if owned is None:
        letters = ['']
    else:
        letters = owned.split(',')  # ['H', '']

    embed = discord.Embed(
        title="Letter Box :mailbox:",
        description=f"Collect all the letter of '{WORD}' and get 10,000 <:energylinks:1146372968570691604>",
        colour=discord.Colour.green()
    )

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png'
    )

    if letter in string.ascii_uppercase:
        embed.add_field(
            name=f":regional_indicator_{str(letter).lower()}:",
            value=f'you got the letter {letter}',
            inline=False
        )
    else:
        embed.add_field(
            name=f':cyclone:',
            value=f'WOW! You got a magical word! :magic_wand:\nThis magical word will randomly transform into any of'
                  f' the word that is left for your event!',
            inline=False
        )

    for i in range(0, len(letters) - 1):
        # {0: 'O', 1: 'N', 2: 'C', 3: 'E', 4: ':regional_indicator_h:', 5: 'U', 6: 'M', 7: 'A', 8: 'N'}
        if list(progress.values()).index(letters[i]) in progress.keys():
            progress[list(progress.values()).index(letters[i])] = \
                f":regional_indicator_{str(progress[list(progress.values()).index(letters[i])]).lower()}:"
        else:
            print(False)

    msg = ''

    if letter in WORD:
        if letter in progress.values():
            progress[list(progress.values()).index(letter)] = \
                f":regional_indicator_{str(progress[list(progress.values()).index(letter)]).lower()}:"
            print(f'progress: {progress}')
            reword = letter
        else:
            msg = f'You already got this letter earlier'
            refund += 25

    elif letter == '#':
        for key, value in progress.items():
            if value in string.ascii_uppercase:
                progress[list(progress.values()).index(value)] = \
                    f":regional_indicator_{str(progress[list(progress.values()).index(value)]).lower()}:"
                print(f'progress: {progress}')

                embed.add_field(
                    name=f":regional_indicator_{str(value).lower()}:",
                    value=f':magic_wand:your magical word transformed into the letter \'{value}\'',
                    inline=False
                )
                msg = f'You got 100% refund on getting a :magic_wand:magical word!'
                refund += 100
                reword = value
                break
            else:
                pass

    else:
        msg = f'This letter is not in \'{WORD}\''
        refund += 10

    if refund == 0:
        pass
    else:
        embed.add_field(
            name=msg,
            value=f'You got {refund} energy link back for this letter',
            inline=False
        )

    for sub in WORD:
        if sub in progress.values():
            break
        else:
            pass
    else:
        win = True

    if win is True:
        embed.add_field(
            name=f':confetti_ball: CONGRATULATIONS :confetti_ball:',
            value=f'You got all the words in \'{WORD}\'',
            inline=False
        )
        embed.add_field(
            name=f'Reward',
            value='10,000 energy links',
            inline=False
        )
    else:
        pass

    result = ''
    for key, value in progress.items():
        result += f" {value}"

    embed.add_field(
        name=f'Your progress',
        value=f'{result}',
        inline=False
    )
    embed.set_footer(text=f'Opened by {interaction.user}')
    return embed, refund, reword, win


async def show_inventory(items, interaction):
    inventory = items.split(',')
    embed = discord.Embed(
        title="Inventory",
        description=f"{interaction.user.name}'s inventory",
        colour=discord.Colour.dark_gold()
    )
    all_item = ""

    for i in range(0, len(inventory) - 1):
        if len(all_item) < 230:
            if inventory[i] in alphabets:
                all_item += f" :regional_indicator_{str(inventory[i]).lower()}:"
            else:
                all_item += f" {inventory[i]}"
        else:
            all_item += f" :regional_indicator_{str(inventory[i]).lower()}:"
            embed.add_field(
                name=all_item,
                value="",
                inline=False
            )
            all_item = ""

    embed.add_field(
        name=all_item,
        value="",
        inline=False
    )

    return embed


async def update_setup():
    embed = discord.Embed(
        title="What's new?",
        description='setup completed successfully',
        colour=discord.Colour.dark_gray()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1116597822624641035/1134146461186142299/Picture6.png')
    embed.add_field(
        name="• Event Stage 2",
        value="On this stage the chances of getting the event words are increased by 100%\n--> Want to know how?\n"
              "Find it yourself!:magic_wand:",
        inline=False
    )
    embed.add_field(
        name=f'• /events',
        value=f'Use this command and play the updated version',
        inline=False
    )

    return embed
