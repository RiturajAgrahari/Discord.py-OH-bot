import mysql.connector
import discord
import random
import string
from database import energy_link, add_energy_link
from embeds import letter_event, show_inventory


def open_database():
    mydb = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    return mydb


async def get_items(id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"SELECT items from inventory where id = {id}"
    mycursor.execute(sql)
    items = mycursor.fetchall()
    mydb.close()
    return items


async def check_inventory(id, interaction):
    items = await get_items(id)
    print(items)
    if items[0][0] is None:
        await interaction.response.send_message(f'Your inventory is empty\ntry </events:0> to get something!',
                                                ephemeral=True)
    else:
        embed = await show_inventory(str(items[0][0]), interaction)
        await interaction.response.send_message(embed=embed)


async def once_human_event(id, interaction):
    Choices = 'ABCDEFGHIJKLMNOPQRSTUVWXY#'

    energy = await energy_link(id)
    if energy >= 100:
        await reduce_energy_link(id, energy)
        randomletter = random.choice(Choices)
        print(randomletter)
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


async def reduce_energy_link(id, amount):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE profile SET energy_link = {amount - 100} WHERE id = {id}"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def add_item(id, item):
    inv = await get_items(id)
    items = inv[0][0]
    if items is None:
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f"UPDATE inventory SET items = '{item},' WHERE id = {id}"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
    else:
        IT = f"{items}"
        IT += f"{item},"
        print(IT)
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f"UPDATE inventory SET items = '{IT}' WHERE id = {id}"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()


async def update_status(id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'update inventory set status = "Claimed" where id = {id}'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def check_status(id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'SELECT status FROM inventory WHERE id = {id}'
    mycursor.execute(sql)
    status = mycursor.fetchall()[0][0]
    mydb.close()
    return status


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
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE inventory SET items = '{inv}' WHERE id = {id}"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

