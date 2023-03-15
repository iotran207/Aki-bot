from time import sleep
import discord
from discord.ext import commands
import aiohttp
from command.cache.list_color import list_color
import random
import json
class Nettruyen(commands.Cog):
    config = {
        "name": "netruyen",
        "desc": "lệnh giúp bạn có thể đọc truyện online ngay trên discord",
        "use": "doc_truyen <mã truyện> <chapter số>",
        "author": "King.(maku team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def doc_truyen(self,ctx,comicHref:str,chapter:str):
        author_dms = await ctx.author.create_dm()
        params = {
            "comicHref":comicHref,
            "chapter":chapter,
            "apikey":"ntkhang"
        }
        async with self.bot.session.get(f'https://goatbot.me/truyentranh24/doc-truyen',params=params) as get_answer:
            answer = await get_answer.json()
            for x in answer["data"]:
                await author_dms.send(x)
                sleep(2)

    @commands.command()
    async def tim_truyen(self,ctx,*,content:str):
        dem=1
        author_dms = await ctx.author.create_dm()
        params = {
        "q":content,
        "apikey":"ntkhang"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://goatbot.me/truyentranh24/search?',params=params) as get_answer:
                answer = await get_answer.json()
                for x in answer["data"]:
                    await author_dms.send(f"{dem}. **name**:{x['name']}    \n**mã truyện**:{x['href']}")
                    await author_dms.send(f"{x['thumbnail']}")
                    dem=dem+1
                    sleep(2)

async def setup(bot):
    await bot.add_cog(Nettruyen(bot))
