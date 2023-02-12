import discord
from discord.ext import commands
import json
import aiohttp
import random
from command.cache.list_color import list_color 
class Covid19(commands.Cog):
    config = {
        "name": "covid19",
        "desc": "xem thông tin tình hình dịch covid19 ở Việt Nam",
        "use": "covid19",
        'author': "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def covid19(self, ctx):
        try:
            full_url = 'https://api.phamvandien.xyz/covid?country=viet%20nam'
            async with aiohttp.ClientSession() as session:
                get = await session.get(full_url)
                data = await get.text()
            parse_json = json.loads(data)
            data2 = parse_json['data']['dangdieutri']
            data3 = parse_json['data']['ca_nhiem_moi']
            data4 = parse_json['data']['hoiphuc']
            data5 = parse_json['data']['total']
            data6 = parse_json['data']['tong_ca_tu_vong']
            em = discord.Embed(title="_Thông tin về dịch bệnh Covid-19 tại Việt Nam_", description=f"**Tổng số ca nhiễm: {data5}\nSố ca nhiễm mới: {data3}\nSố ca nhiễm đang điều trị: {data2}\nSố ca đã hổi phục: {data4}\nTổng số ca tử vong: {data6}**", color = random.choice(list_color))
            em.set_author(name = ctx.author.name, icon_url=ctx.author.display_avatar.url)
            em.set_footer(text=f"yêu cầu từ {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed = em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Covid19(bot))
