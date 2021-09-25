import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

class music(commands.Cog):
    def __init__(self, bot):
        
        self.ydl_opt = {
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
        self.ffmpeg_opts = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
                }

        self.bot = bot
        self.is_playing = False
        self.queue = []
        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.ydl_opt) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            url =  self.queue[0][0]['source']
            self.queue.pop(0)

            self.vc.play(discord.FFmpegOpusAudio(url, **self.ffmpeg_opts), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.queue) > 0:
            self.is_playing = True

            url =  self.queue[0][0]['source']
            
            if self.vc == "" or not self.vc.is_connected():
                self.vc = await self.queue[0][1].connect()
            else:
                self.vc = await self.bot.move_to(self.queue[0][1])
                
            self.queue.pop(0)

            self.vc.play(discord.FFmpegOpusAudio(url, **self.ffmpeg_opts), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command()
    async def p(self, ctx, *args):
        query = " ".join(args)

        videosSearch = VideosSearch(*args, limit=1)

        embed1 = discord.Embed(
            title = videosSearch.result()['title'][0],
            description = videosSearch.result()['link'][0],
            colour = discord.Colour.blurple()
        )

        embed1.set_thumbnail(url=videosSearch.result()['thumbnails'][0])

        vc = ctx.author.voice.channel
        if vc is None:
            await ctx.send("You're not in the voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Error! Could not download song.")
            else:
                await ctx.send(embed=embed1)
                self.queue.append([song, vc])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await ctx.message.add_reaction("⏭️")
            await self.play_music()

    @commands.command()
    async def pause(self, ctx):
        await ctx.message.add_reaction('⏸')
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        await ctx.message.add_reaction('⏯')
        await ctx.voice_client.resume()

    @commands.command()
    async def dc(self, ctx):
        await ctx.message.add_reaction('⏏️')
        await ctx.voice_client.disconnect()

    
