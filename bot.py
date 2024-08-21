import discord
from discord.ext import commands, tasks, voice_recv
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


@bot.hybrid_command(description= "Ping!")
async def ping(ctx):
    await ctx.send('Pong')


@bot.hybrid_command(description="Joins the vc channel you are in")
async def joinvc(ctx):
    await ctx.send('Joining!')
    if not ctx.author.voice:
        await ctx.send('Channel not found')
        return
    destination = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_state.voice.move_to(destination)
        return
    await destination.connect()
    await ctx.send("Successfully joined the voice channel.")

@bot.hybrid_command(description="Leaves the vc channel the bot is in")
async def leavevc(ctx):
    await ctx.send('Leaving!')
    if ctx.voice_client:
        await ctx.voice_client.disconnect()


@bot.hybrid_command(description="Joins a channel and transcribes the audio in it")
async def transcribe(ctx):
    def callback(user, data: voice_recv.VoiceData):
            print(f"Got packet from {user}")
            print(data)
            # print (f"Here's data hopefully(?){ext_data}")


    if not ctx.author.voice:
        await ctx.send('Channel not found')
        return

    if ctx.voice_client:
        # Documentation for discord voice library requires us to connect with voice_recv... every time to enable audio
        await ctx.voice_client.disconnect()

    vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
    vc.listen(voice_recv.BasicSink(callback))
    await ctx.send(F"Here's the data ")

Token = os.getenv('TOKEN')
bot.run(Token)
