import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import youtube_dl
import ctypes
import ctypes.util

load_dotenv()

youtube_dl.utils.bug_reports_message = lambda: ''

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

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix = '.', intents = intents)

queue = []

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
        await asyncio.sleep(1)
        await voice_state.disconnect()

@client.command()
async def dc(ctx):
    await ctx.message.add_reaction('⏏️')
    await ctx.voice_client.disconnect()

@client.command()
async def p(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in the voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    ctx.voice_client.stop()
    
    vc = ctx.voice_client
        
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(queue, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
        vc.play(source)
        del(queue[0])

@client.command()
async def queue(ctx, url):
    queue.append(url)
    await ctx.send(f'`{url}` added to the queue!')

@client.command()
async def remove(ctx, number):
    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    except:
        await ctx.send('Your queue is either empty or the index of the list is out of range!')

@client.command()
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@client.command()
async def pause(ctx):
    await ctx.message.add_reaction('⏸')
    await ctx.voice_client.pause()

@client.command()
async def resume(ctx):
    await ctx.message.add_reaction('▶️')
    await ctx.voice_client.resume()

@client.command()
async def cover(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in the voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    ctx.voice_client.stop()
    
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if url.lower() == "chugjug":
            info = ydl.extract_info("https://youtu.be/qwJxr1TDhgU", download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)

        elif url.lower() == "takeonme":
            info = ydl.extract_info("https://youtu.be/Ze2xWPksgF0", download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)

        elif url.lower() == "gloop":
            info = ydl.extract_info("https://youtu.be/o-ofNGM5dI8", download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)

        elif url.lower() == "revenge":
            info = ydl.extract_info("https://youtu.be/Ifb-O5DoDVA", download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)

        elif url.lower() == "rick":
            info = ydl.extract_info("https://youtu.be/zbr78RvPoYk", download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)


client.run(os.getenv('BOT_TOKEN'))