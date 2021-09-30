import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
from youtubesearchpython.__future__ import VideosSearch


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
                self.vc.move_to(self.queue[0][1])
                
            self.queue.pop(0)

            self.vc.play(discord.FFmpegOpusAudio(url, **self.ffmpeg_opts), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    @commands.command()
    async def p(self, ctx, *, search_terms):

        videosSearch = VideosSearch(search_terms, limit=1)
        videosResult = await videosSearch.next()
        url = videosResult['result'][-1]['link']

        embed1 = discord.Embed(
            title = "Song Queued",
            description = videosResult['result'][0]['title'],
            colour = discord.Colour.blurple()
        )

        embed1.set_thumbnail(url=videosResult['result'][0]['thumbnails'][0]['url'])

        voice_channel = ctx.author.voice.channel
        
        if ctx.voice_state.voice is None:
            await ctx.send("You're not in the voice channel!")
        else:
            song = self.search_yt(url)
            if type(song) == type(True):
                await ctx.send("Could not download song due to age restrictions or error finding video.")
            else:
                await ctx.send(embed=embed1)
                self.queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

        bot_deafen = ctx.guild.get_member(875675890523185202)
        await bot_deafen.edit(deafen=True)

    
    @commands.command()
    async def q(self, ctx):
        queue_list = []
        for count, value in enumerate(self.queue, 0):
            queue_list.append(self.queue[count][0]['title'] + "\n")
        if queue_list is not None:
            for count, value in enumerate(queue_list, 1):
                await ctx.send("Track " + str(count) + ": " + value)
        elif queue_list is None:
            await ctx.send("No queued songs.")


    @commands.command()
    async def r(self, ctx, *, track_number):
        queue_list = []
        for count, value in enumerate(self.queue, 0):
            queue_list.append(self.queue[count][0]['title'] + "\n")
        if queue_list is not None:
            for count, value in enumerate(queue_list, 1):
                if str(track_number) == str(count):
                    count -= 1
                    self.queue.pop(count)
                    await ctx.send("Removed song from queue!")
        else:
            await ctx.send("Error removing song from queue.")


    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music()
            await ctx.message.add_reaction("⏭️")
            

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        if ctx.voice_client.is_paused() is True:
            await ctx.message.add_reaction('⏸')


    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        if ctx.voice_client.is_paused() is False:
            await ctx.message.add_reaction('⏯')
        else:
            pass


    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()
        if ctx.voice_client is None:
            await ctx.message.add_reaction('⏏️')
        else:
            pass