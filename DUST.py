# -*- coding: utf-8 -*-
#Auto Loop
import discord
from discord.ext import commands
from discord.utils import get
import sqlite3
import os
import random
import asyncio

TOKEN = ''
BOT_PREFIX = '.mj'

bot = commands.Bot(command_prefix=BOT_PREFIX)
DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
SQL = db.cursor()

START_BALANCE = 10000
C_NAME = "DUST"





@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game(".mj도움말")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(pass_context=True, brief="유저의 지갑을 보여줍니다.")
async def 내지갑(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        await ctx.send(f"{ctx.message.author.mention}님! {C_NAME}에 가입이 안되있으셔서 시작금액을 지급해드렸어요.")
        db.commit()
        return
    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    SQL.execute(f'UPDATE Accounts set user_name = "{USER_NAME}" where user_id = "{USER_ID}"')
    await ctx.send(f"{ctx.message.author.mention}님은 {result_userbal[0]} {C_NAME}가 있어요")


@bot.command(pass_context=True, brief="유저의 지갑을 보여줍니다.")
async def 지갑(ctx, user: discord.Member):
    USER_ID = user.id
    USER_NAME = str(user)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        await ctx.send(f"<@{user.id}>님! {C_NAME}에 가입이 안되있으셔서 시작금액을 지급해드렸어요.")
        db.commit()
        return
    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    SQL.execute(f'UPDATE Accounts set user_name = "{USER_NAME}" where user_id = "{USER_ID}"')
    await ctx.send(f"<@{user.id}>님은 {result_userbal[0]} {C_NAME}가 있어요")

@bot.command(pass_context=True, brief="돈을 줍니다.")
async def 돈줘(ctx, amount: int):
    if ctx.author.id == 380625576014381060:
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)
        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        if result_userID is None:
            SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
            await ctx.send(f"{ctx.message.author.mention}님! {C_NAME}에 가입이 안되있으셔서 시작금액을 지급해드렸어요.")
            db.commit()
            return
        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, USER_ID))
        db.commit()
        await ctx.send(f"{ctx.message.author.mention}님이 {amount} {C_NAME}를 받았습니다.")
    else:
        await ctx.send("당신은 권한이 없습니다!")
        return

@bot.command(pass_context=True, brief="룰렛")
async def 배팅(ctx, amount: int):
    randomNum = random.randrange(1, 3)
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    max_balance = 1000
    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"{ctx.message.author.mention}님! 당신의 배팅금액을 {result_userbal[0]} {C_NAME}보다 높게 설정하셨어요!")
        return
    if randomNum==1:
        await ctx.send("배팅중....")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💵")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💴")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💶")
        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, USER_ID))
        db.commit()
        await ctx.send(f"{ctx.message.author.mention}님이 배팅에 성공하셔서 {amount} {C_NAME}를 받으셨습니다.")
        await ctx.message.add_reaction("💰")
    else:
        await ctx.send("배팅중....")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💵")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💴")
        await asyncio.sleep(0.7)
        await ctx.message.add_reaction("💶")
        SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
        SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = SQL.fetchone()
        SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, USER_ID))
        db.commit()
        await ctx.send(f"{ctx.message.author.mention}님이 배팅에 실패하셔서 {amount} {C_NAME}를 잃으셨습니다.")
        await ctx.message.add_reaction("💸")

@bot.command(pass_context=True, brief="룰렛")
async def 돈지급(ctx):
    amount = 1000
    moneyd = 1
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    result_userID = SQL.fetchone()
    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        await ctx.send(f"{ctx.message.author.mention}님! {C_NAME}에 가입이 안되있으셔서 시작금액을 지급해드렸어요.")
        db.commit()
        return
    if moneyd > int(result_userbal[0]):
        await ctx.send(f"{ctx.message.author.mention}님의 {C_NAME}이 없으셔서 {amount} {C_NAME}를 지급해드렸어요.")
        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, USER_ID))
        db.commit()
        return
    else:
        await ctx.send(f"{ctx.message.author.mention}님은 {C_NAME}가 있어요.")

@bot.command(pass_context=True, brief="돈을 송금합니다.", aliases=["전송"])
async def 송금(ctx, other: discord.Member, amount: int):
    if amount < 0:
        await ctx.send("-는 사용하실 수 없습니다!.")
        return
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    OTHER_ID = other.id
    OTHER_NAME = str(other)

    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
    result_otherID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        db.commit()
    if result_otherID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, START_BALANCE))
        db.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"{ctx.message.author.mention}님의 잔액은 {amount} {C_NAME}보다 적어서 보낼 수 없어요.")
        return

    SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, USER_ID))
    db.commit()
    SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, OTHER_ID))
    db.commit()

    await ctx.send(f"{ctx.message.author.mention}님이 {other.mention}님에게 {amount} {C_NAME}를 보냈습니다.")


@bot.command(pass_context=True, brief="순위를 보여줍니다.")
async def 순위(ctx):
    try:
        SQL.execute(f"select user_name, balance from Accounts order by balance desc")
        result_top10 = SQL.fetchmany(10)

        embed = discord.Embed(
            colour=discord.Colour.gold()
        )

        embed.set_author(name="순위")
        embed.add_field(name="#1", value=f"이름: {result_top10[0][0]} 잔액: {result_top10[0][1]}", inline=False)
        embed.add_field(name="#2", value=f"이름: {result_top10[1][0]} 잔액: {result_top10[1][1]}", inline=False)
        embed.add_field(name="#3", value=f"이름: {result_top10[2][0]} 잔액: {result_top10[2][1]}", inline=False)
        embed.add_field(name="#4", value=f"이름: {result_top10[3][0]} 잔액: {result_top10[3][1]}", inline=False)
        embed.add_field(name="#5", value=f"이름: {result_top10[4][0]} 잔액: {result_top10[4][1]}", inline=False)
        embed.add_field(name="#6", value=f"이름: {result_top10[5][0]} 잔액: {result_top10[5][1]}", inline=False)
        embed.add_field(name="#7", value=f"이름: {result_top10[6][0]} 잔액: {result_top10[6][1]}", inline=False)
        embed.add_field(name="#8", value=f"이름: {result_top10[7][0]} 잔액: {result_top10[7][1]}", inline=False)
        embed.add_field(name="#9", value=f"이름: {result_top10[8][0]} 잔액: {result_top10[8][1]}", inline=False)
        embed.add_field(name="#10", value=f"이름: {result_top10[9][0]} 잔액: {result_top10[9][1]}", inline=False)



        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            colour=discord.Colour.gold()
        )

        embed.set_author(name="오류!")
        embed.add_field(name="``죄송합니다.``", value="DUST를 이용하는 사람이 최소 10명 이상이 되야지 순위를 보여드릴 수 있어요.", inline=False)
        await ctx.send(embed=embed)
@bot.command()
async def about(ctx):
    embed = discord.Embed(colour=discord.Colour.gold())
    embed.set_author(name="DUST란")
    embed.add_field(name="``about``", value="DUST는 가상으로 만든 디스코드 코인입니다. ``가치 없음``", inline=False)
    embed.set_footer(text="먼지#3536")
    
    await ctx.send(embed=embed)

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(colour=discord.Colour.gold())
    embed.set_author(name="도움말")
    embed.add_field(name="``명령어``", value=".mjabout, .mj돈지급, .mj송금 [코인 갯수], .mj내지갑, .mj지갑 [@멘션 필수!], .mj순위, .mj배팅 [코인 갯수]", inline=False)
    embed.add_field(name="``시작시 주의사항``", value=".mj내지갑을 치셔야지 정상적으로 시작가입금액 10000 DUST가 충전됩니다.", inline=False)
    embed.set_footer(text="먼지#3536")
    
    await ctx.send(embed=embed)



bot.run(TOKEN)