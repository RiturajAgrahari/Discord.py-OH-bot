import mysql.connector
import discord
import random
import itertools


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
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    return mydb


async def checking_main_profile(interaction):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'select id from profile where discord_id = "{interaction.user.mention}"'
    mycursor.execute(sql)
    test = mycursor.fetchall()
    mydb.close()
    if len(test) == 0:
        print(f'creating {interaction.user.name} profile...')
        return await creating_main_profile(interaction.user.name, interaction.user.mention)
    else:
        print(f'{interaction.user.name} profile already exist in database...')
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


async def energy_link(id):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'select energy_link from profile where id = {id}'
    mycursor.execute(sql)
    energy_link = mycursor.fetchall()[0][0]
    mydb.close()
    return energy_link


async def add_energy_link(uid, coins):
    mydb = open_database()
    energy = await energy_link(uid)
    mycursor = mydb.cursor()
    total = energy + coins
    sql = f'update profile set energy_link = {total} where id = {uid}'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    return coins


async def check_time(T, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'select status from profile where id = {uid}'
    mycursor.execute(sql)
    time = mycursor.fetchall()[0][0]
    mydb.close()
    if (T - time) < 24 * 60 * 60:
        gap = T - time
        return False, gap
    else:
        await update_status(T, uid)
        return True, 0


async def update_status(T, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'update profile set status = {T} where id = {uid}'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def all_game_profile(game_name, pl_id, pl_stat):  # (game_name, [1, 2])
    for (uid, stat) in zip(pl_id, pl_stat):
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f'select * from {game_name} where id = {uid}'
        mycursor.execute(sql)
        test = mycursor.fetchall()
        mydb.close()
        if len(test) == 0:
            print(f"creating {uid}'s rock paper scissor profile...")
            await creating_in_game_profile(game_name, uid, stat)
        else:
            print(f'{uid} rock paper scissor profile already exist in database...')
            await update_data(game_name, stat, uid)


async def creating_in_game_profile(game_name, uid, stat):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {game_name} (id) VALUES (%s)"
    val = [(uid)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    await update_data(game_name, stat, uid)


async def update_data(game_name, stat, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'update {game_name} set {stat} = {stat} + 1 where id = {uid}'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


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
