import discord
import aiohttp
from discord.ext import commands
import random
from commands.cache.list_color import list_color
import json
class Thinh(commands.Cog):
    config = {
      "name": "thinh",
      "desc": "thính+))",
      "use": "thinh",
      "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def thinh(self, ctx):
        try:
            type = random.choice(["boy", "girl"])
            links = ["https://raw.githubusercontent.com/ledingg1997/ledingg-/main/datathinh.json", f"https://www.nguyenmanh.name.vn/api/thathinh?type={type}"]
            url = random.choice(links)
            if url == links[0]:
                async with aiohttp.ClientSession() as session:
                    get = await session.get(url)
                    data = json.loads(await get.text())
                    result = data["data"][f"{random.randint(1, 187)}"]
                    em = discord.Embed(title=f"**{result}**",color=random.choice(list_color))
                    em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
                    await ctx.reply(embed = em)
                    return 
            async with aiohttp.ClientSession() as session:
                get = await session.get(url)
                data = await get.json()
                result = data["result"]["data"]
                em = discord.Embed(title=f"**{result}**",color=random.choice(list_color))
                em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
                await ctx.reply(embed = em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Thinh(bot))           
