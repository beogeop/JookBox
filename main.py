import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from music import music

load_dotenv()

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-p"))
    print('Logged in as {0.user}'.format(bot))

bot.add_cog(music(bot))

bot.run(os.getenv('BOT_TOKEN'))