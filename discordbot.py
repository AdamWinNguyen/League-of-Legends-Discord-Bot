import os
import discord
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
#import pandas as pd
import json

load_dotenv()
DTOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

RTOKEN = os.getenv('RIOT_TOKEN')
watcher = LolWatcher(RTOKEN)
region = 'na1'
me = watcher.summoner.by_name(region, 'EvilSteel')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('~rank'):
        rankJSON = watcher.league.by_summoner(region, me['id'])
        response = json.dumps(rankJSON)
        await message.channel.send(response['tier'] + ' ' + response['rank'])

client.run(DTOKEN)
