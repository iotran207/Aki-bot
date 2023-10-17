import discord
from discord.ext import commands
import json
import aiohttp
import random
from commands.cache.list_color import list_color 
class Covid19(commands.Cog):
    config = {
        "name": "covid19",
        "desc": "xem thông tin tình hình dịch covid19 ở Việt Nam",
        "use": "covid19",
        'author': "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def covid19(self, ctx):
        try:
            full_url = 'https://static.pipezero.com/covid/data.json'
            async with aiohttp.ClientSession() as session:
                get = await session.get(full_url)
                data = await get.text()
            data = json.loads(data)["total"]["internal"]
            total = data["cases"]
            recovered = data["recovered"]
            death = data["death"]
            em = discord.Embed(title="_Thông tin về dịch bệnh Covid-19 tại Việt Nam_", description=f"**Tổng số ca nhiễm: {total}\nSố ca đã hổi phục: {recovered}\nTổng số ca tử vong: {death}**", color = random.choice(list_color))
            em.set_author(name = ctx.author.name, icon_url=ctx.author.display_avatar.url)
            em.set_footer(text=f"yêu cầu từ {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed = em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Covid19(bot))
