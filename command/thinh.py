import discord
import aiohttp
from discord.ext import commands
import json
import random
class Thinh(commands.Cog):
    config = {
      "name": "thinh",
      "desc": "thính+))",
      "use": "thinh",
      "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def thinh(self, ctx):
        type = random.choice(["boy", "girl"])
        links = ["https://raw.githubusercontent.com/ledingg1997/ledingg-/main/datathinh.json", f"https://www.nguyenmanh.name.vn/api/thathinh?type={type}"]
        url = random.choice(links)
        if url == links[0]:
            async with aiohttp.ClientSession() as session:
                get = await session.get(url)
                data = json.loads(await get.text())
                await ctx.reply(data["data"][f"{random.randint(1, 187)}"])
                return 
        async with aiohttp.ClientSession() as session:
            get = await session.get(url)
            data = await get.json()
            await ctx.reply(data["result"]["data"])
async def setup(bot):
    await bot.add_cog(Thinh(bot))           
