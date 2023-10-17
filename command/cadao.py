import discord
from discord.ext import commands
import aiohttp
import random
from command.cache.list_color import list_color
class Cadao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cadao(self, ctx):
        config = {
            "name": "cadao",
            "desc": "ca dao Việt Nam;)",
            "use": "cadao",
            "author": "Anh Duc(aki team)"
        }
        try:
            async with aiohttp.ClientSession() as session:
                list = await session.get("https://gist.githubusercontent.com/tuyenld/da9d7c7ed285c3aa6f0853e69b00cb17/raw/e8c927e3a053611ce4e65fbe434bab222321e481/cadao-tuc-ngu.txt")
                list = await list.text()
                list = list.split("**")
                result = random.choice(list)
                em = discord.Embed(title=f"**Ca dao Việt Nam**",description = f"_{result}_",color=random.choice(list_color))
                em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
                await ctx.reply(embed = em)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Cadao(bot))
