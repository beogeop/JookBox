import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import youtube_dl
from youtube_search import YoutubeSearch
import json
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

queue = []

intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".p"))
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
async def p(ctx, *, search_terms):
    
    if ctx.author.voice is None:
        await ctx.send("You're not in the voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    ctx.voice_client.stop()
    vc = ctx.voice_client
    
    results = YoutubeSearch(search_terms, max_results = 1).to_json()

    embed1 = discord.Embed(
        title = 'Currently Playing',
        description = str(json.loads(results)['videos'][0]['title']),
        colour = discord.Colour.blue()
    )

    embed1.set_thumbnail(url=str(json.loads(results)['videos'][0]['thumbnails'][0]))

    embed2 = discord.Embed(
        title = 'Queued',
        description = str(json.loads(results)['videos'][0]['title']),
        colour = discord.Colour.purple()
    )

    embed2.set_thumbnail(url=str(json.loads(results)['videos'][0]['thumbnails'][0]))

    try:
        yt_id = str(json.loads(results)['videos'][0]['id'])
        yt_url = "https://www.youtube.com/watch?v=" + yt_id
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_opts)
            vc.play(source)
            await ctx.send(embed=embed1)
    except:
        pass
        print("No results found.")
    
@client.command()
async def pause(ctx):
    await ctx.message.add_reaction('⏸')
    await ctx.voice_client.pause()

@client.command()
async def resume(ctx):
    await ctx.message.add_reaction('▶️')
    await ctx.voice_client.resume()

client.run(os.getenv('BOT_TOKEN'))