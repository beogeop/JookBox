import discord
from discord.ext import commands
import os
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client)) 

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
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
    }

    ffmpeg_opt = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opt)
        vc.play(source)

@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused!")

@client.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resumed!")

client.run(os.getenv('BOT_TOKEN'))