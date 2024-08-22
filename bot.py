import discord
from discord.ext import commands, tasks, voice_recv
import vosk
import pyaudio
import os
from dotenv import load_dotenv
import pyogg


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

discord.opus._load_default()

model= "./stt_model"
recognizer= vosk.KaldiRecognizer


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

# Worth mentioning that discord doesn't support
@bot.hybrid_command(description="Joins a channel and transcribes the audio in it")
async def transcribe(ctx):
    buffer = []

    def flush(buffer):
        print(buffer)
        buffer.clear()
        # print (F"Empty buffer:{buffer}")


    def audio_processing_callback(user, data: voice_recv.VoiceData):
            print(f"Got packet from {user}")
            # print(dir(data))
            buffer.append(data.packet)
            # print(data.packet)
            if len(buffer) > 45:
                flush(buffer)
    if not ctx.author.voice:
        await ctx.send('Channel not found')
        return

    if ctx.voice_client:
        # Documentation for discord voice library requires us to connect with voice_recv... every time to enable audio
        await ctx.voice_client.disconnect()

    vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
    # vc.wants_opus(False)
    # print(dir(voice_recv.BasicSink))
    vc.listen(voice_recv.BasicSink(audio_processing_callback))
    await ctx.send(F"Transcribing!")

Token = os.getenv('TOKEN')
bot.run(Token)
