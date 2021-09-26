import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from music import music

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '-', intents = intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-p"))
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return
    if len(voice_state.channel.members) == 1:
        await asyncio.sleep(1)
        await voice_state.disconnect()



bot.add_cog(music(bot))

bot.run(os.getenv('BOT_TOKEN'))