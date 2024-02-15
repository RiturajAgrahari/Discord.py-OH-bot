import mysql.connector
import discord
import random
import string
from database import check_energy_link, add_energy_link, select_query, update_query
from embeds import letter_event, show_inventory

async def get_items(id):
    items = await select_query(column='items', table='inventory', condition_column='id', condition_value=id)
    return items


async def check_inventory(id, interaction):
    items = await get_items(id)
    print(items)
    if items[0][0] is None:
        await interaction.response.send_message(f'Your inventory is empty\ntry </events:1139936270810882074> to get something!',
                                                ephemeral=True)
    else:
        embed = await show_inventory(str(items[0][0]), interaction)
        await interaction.response.send_message(embed=embed)


async def once_human_event(id, interaction):
    Choices = 'ABCDEFGHIJKLMNOPQRSTUVWXY#'

    energy = await check_energy_link(id)
    if energy >= 100:
        await reduce_energy_link(id)
        randomletter = random.choice(Choices)
        items = await get_items(id)
        embed, refund, reword, win = await letter_event(interaction, randomletter, items[0][0])
        await add_energy_link(id, refund)

        if reword is False:
            pass
        else:
            print(f'{reword} is added in inventory!')
            await add_item(id, reword)
        await interaction.response.send_message(embed=embed)

        if win is True:
            await add_energy_link(id, 10000)
            await update_status(id)
            await remove_inventory(id, 'ONCEHUMAN')
            await add_item(id, '🏅')
        else:
            pass
    else:
        await interaction.response.send_message(f'You need 100 <:energylinks:1146372968570691604> to open a letter box',
                                                ephemeral=True)


async def reduce_energy_link(id):
    await update_query(table='profile', key_value={'energy_link': 100}, condition_column='id', condition_value=id, operation='subtraction')

async def add_item(id, item):
    inv = await get_items(id)
    items = inv[0][0]
    if items is None:
        await update_query(table='inventory', key_value={'items': f'{items},'}, condition_column='id', condition_value=id)
        # sql = f"UPDATE inventory SET items = '{item},' WHERE id = {id}"
    else:
        IT = f"{items}"
        IT += f"{item},"
        await update_query(table='inventory', key_value={'items': f'{IT}'}, condition_column='id', condition_value=id)
        # sql = f"UPDATE inventory SET items = '{IT}' WHERE id = {id}"



async def update_status(id):
    await update_query(table='inventory', key_value={'status': 'Claimed'}, condition_column='id', condition_value=id)

async def check_event_status(id):
    status = await select_query(column='status', table='inventory', condition_column='id', condition_value=id)
    return status[0][0]


async def remove_inventory(id, object):
    items = await get_items(id)
    inventory = str(items[0][0]).split(',')
    print(inventory)
    for z in object:
        try:
            inventory.remove(z)
        except Exception as e:
            print(e)
    print(inventory)
    await update_inventory(id, inventory)


async def update_inventory(id, inventory):
    inv = ""
    for i in range(0, len(inventory)):
        if i < len(inventory) - 1:
            inv += f"{inventory[i]},"
        else:
            continue
    print(inv)
    await update_query(table='inventory', key_value={'items': f'{inv}'}, condition_column='id', condition_value=id)




