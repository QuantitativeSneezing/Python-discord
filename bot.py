import discord
from discord.ext import commands, tasks
import vosk
import pyaudio
import json
import os
from dotenv import load_dotenv


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

Token = os.getenv('TOKEN')
client.run(Token)
