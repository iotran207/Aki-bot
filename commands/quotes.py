import discord
from discord.ext import commands
import aiohttp
from commands.cache.list_color import list_color
import random
class Quotes(commands.Cog):
    config = {
        "name": "quotes",
        "desc": "Tổng hợp những câu nói hay của các vĩ nhân nổi tiếng và của những chúa tể ngôn từ Việt nam",
        "use": "quotes",
        "author": 'Anh Duc(aki team)'
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def quotes(self, ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            quote = await session.get("https://api.aggstrawvn.repl.co/quotes")
            quote = await quote.json()
            result = quote["result"]
            em = discord.Embed(title="**Best Quotes**", description = f"_{result}_", color=random.choice(list_color))
            em.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=em)
async def setup(bot):
    await bot.add_cog(Quotes(bot))