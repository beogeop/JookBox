import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import youtube_dl
import ctypes
import ctypes.util

load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".play"))
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return
    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()

@client.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("You're not in the voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    ctx.voice_client.stop()
    vc = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0',
    }

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opt)
        vc.play(source)

@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()

@client.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    
client.run(os.getenv('BOT_TOKEN'))