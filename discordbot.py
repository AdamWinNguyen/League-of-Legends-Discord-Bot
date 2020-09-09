import os
import discord
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
#import pandas as pd
import json
from discord.ext import commands

load_dotenv()
DTOKEN = os.getenv('DISCORD_TOKEN')

RTOKEN = os.getenv('RIOT_TOKEN')
watcher = LolWatcher(RTOKEN)
REGION = os.getenv('REGION')

bot = commands.Bot(command_prefix='~')


@bot.command(name='rank')
async def rank(ctx, username: str):
    me = watcher.summoner.by_name(REGION, username)
    rankJSON = watcher.league.by_summoner(REGION, me['id'])
    ranked = False
    i = 0
    while i < len(rankJSON):
        response = rankJSON[i]
        if response['queueType'] == 'RANKED_SOLO_5x5':
            ranked = True
            break
        i += 1
    if ranked:
        await ctx.send(response['tier'] + ' ' + response['rank'] + ' ' + str(response['leaguePoints']) + ' LP')
    else:
        await ctx.send('This user is unranked.')

@bot.command(name='create')
async def create(ctx):
    servername = ctx.message.guild.name
    try:
        os.makedirs('ServerLeaderboards')
    except FileExistsError:
        pass
    open('ServerLeaderboards\\' + servername + '.txt', 'w+')
    await ctx.send('Leaderboard generated')


bot.run(DTOKEN)
