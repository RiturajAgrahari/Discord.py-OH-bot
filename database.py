import mysql.connector
import discord
import random
import itertools
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MY_SQL_HOST")
USER = os.getenv("MY_SQL_USER")
PASSWORD = os.getenv("MY_SQL_PASSWORD")
DATABASE = os.getenv("MY_SQL_DATABASE")


# Need to add multiple columns and conditions!
async def select_query(column: str, table: str, condition_column: str = None, condition_value: str | int = None,
                       order_by_column: str = None, ascending: bool = True, limit: int = None, offset: int = 0):
    sql = f"SELECT {column} FROM {table}"

    if condition_column is None or condition_value is None:
        pass
    else:
        if type(condition_value) is str:
            sql += f" WHERE {condition_column} = '{condition_value}'"
        else:
            sql += f" WHERE {condition_column} = {condition_value}"

    if order_by_column is None:
        pass
    else:
        sql += f" ORDER BY {order_by_column}"

    if not ascending:
        sql += " DESC"

    if limit:
        sql += f" LIMIT {offset}, {limit}"

    mydb = open_database()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    output = mycursor.fetchall()
    mydb.close()
    return output


# Need to add multiple conditions!
async def update_query(table:str, key_value:dict, condition_column:str=None, condition_value:str | int=None, operation:str='equal'):
    # {'koens': 100}
    if condition_column is None or condition_value is None:
        condition = ""
    else:
        if type(condition_value) is str or type(condition_value) is None:
            condition = f" WHERE {condition_column} = '{condition_value}'"
        else:
            condition = f" WHERE {condition_column} = {condition_value}"

    set = ""

    for key, value in key_value.items():
        if type(value) is str:
            set += f", {key} = '{value}'"

        elif type(value) is int:
            if operation == 'equal':
                set += f", {key} = {value}"
            elif operation == 'addition':
                set += f", {key} = {key} + {value}"
            elif operation == 'subtraction':
                set += f", {key} = {key} - {value}"
            else:
                print('wrong operation!')
        else:
            print('wrong value datatype')


    set = set.lstrip(',')

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE {table} SET{set}{condition}"
    # print(f"(sql update query): {sql}")
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


class profile:
    def __init__(self, discord_id, var):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'select * from profile where {var} = "{discord_id}";'
        mycursor.execute(sql)
        set = mycursor.fetchall()[0]
        mydb.close()
        self.id = set[0]
        self.name = set[1]
        self.discord_id = set[2]
        self.energy_link = set[3]
        self.time = set[4]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_discord_id(self):
        return self.discord_id

    def get_energy_link(self):
        return self.energy_link

    def get_time(self):
        return self.time

def open_database():
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    return mydb

async def checking_main_profile(interaction):
    test = await select_query(column='id', table='profile', condition_column='discord_id', condition_value=interaction.user.mention)
    if len(test) == 0:
        print(f'creating {interaction.user.name} profile...')
        return await creating_main_profile(interaction.user.name, interaction.user.mention)
    else:
        return test[0][0]


async def creating_main_profile(name, discord_id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = "INSERT INTO profile (name, discord_id, energy_link, status) VALUES (%s, %s, %s, %s)"
    val = [(name, discord_id, 0, 0)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()
    a = profile(discord_id, 'discord_id')
    await create_inventory(a.get_id())
    return a.get_id()


async def create_inventory(id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO inventory (id) VALUES (%s)"
    val = [(id)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

async def all_game_profile(game_name, pl_id, pl_stat):  # (game_name, [1, 2])
    for (uid, stat) in zip(pl_id, pl_stat):
        test = await select_query(column='*', table=game_name, condition_column='id', condition_value=uid)
        if len(test) == 0:
            print(f"creating {uid}'s rock paper scissor profile...")
            await creating_in_game_profile(game_name, uid, stat)
        else:
            await update_query(table=game_name, key_value={stat: 1}, condition_column='id', condition_value=uid, operation='addition')


async def creating_in_game_profile(game_name, uid, stat):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {game_name} (id) VALUES (%s)"
    val = [(uid)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    await update_query(table=game_name, key_value={stat: 1}, condition_column='id', condition_value=uid,
                       operation='addition')


class leaderboard_data:
    def __init__(self, game):
        self.game = game

    def win_board(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, wins FROM {self.game} ORDER BY wins DESC LIMIT 10;'
        mycursor.execute(sql)
        win_data = mycursor.fetchall()
        mydb.close()
        return win_data

    def loss_board(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, loss FROM {self.game} ORDER BY loss DESC LIMIT 10;'
        mycursor.execute(sql)
        loss_data = mycursor.fetchall()
        mydb.close()
        return loss_data

    def tie_board(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, tie FROM {self.game} ORDER BY tie DESC LIMIT 10;'
        mycursor.execute(sql)
        tie_data = mycursor.fetchall()
        mydb.close()
        return tie_data

    def win_rate(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, wins/(wins + loss + tie) AS win_rate FROM {self.game} ORDER BY win_rate DESC LIMIT 10;'
        mycursor.execute(sql)
        rate_data = mycursor.fetchall()
        mydb.close()
        return rate_data

    def win_rate2(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, wins/(wins + loss) AS win_rate FROM {self.game} ORDER BY win_rate DESC LIMIT 10;'
        mycursor.execute(sql)
        rate_data = mycursor.fetchall()
        mydb.close()
        return rate_data

    def energy_links(self):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'SELECT id, energy_link FROM profile ORDER BY energy_link DESC LIMIT 10;'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.close()
        return data


async def check_status(uid):
    status = await select_query(column='status', table='profile', condition_column='id', condition_value=int(uid))
    return status[0][0]

async def add_energy_link(value, uid):
    await update_query(table='profile', key_value={'energy_link': value}, condition_column='id', condition_value=uid, operation='addition')

async def update_status(uid):
    await update_query(table='profile', key_value={'status': 'claimed'}, condition_column='id', condition_value=uid)

async def reset_data():
    await update_query(table='profile', key_value={'status': 'not_claimed'})

async def check_energy_link(uid):
    energy_link = await select_query(column='energy_link', table='profile', condition_column='id', condition_value=uid)
    return energy_link[0][0]
