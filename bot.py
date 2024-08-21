import discord
from discord.ext import commands, tasks
import vosk
import pyaudio
import os
from dotenv import load_dotenv


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.hybrid_command(description="join the vc channel you are in")
async def joinvc(ctx, message):
    await ctx.send('Joining!')

@bot.hybrid_command(description= "Ping!")
async def ping(ctx):
    await ctx.send('Pong')


Token = os.getenv('TOKEN')
bot.run(Token)
