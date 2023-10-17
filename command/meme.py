import discord
from discord.ext import commands
import aiohttp
class Meme(commands.Cog):
    config = {
        "name": "meme",
        "desc": "gui mot meme bat ki o moi the loai",
        "use": "meme",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def meme(self, ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            get = await session.get("https://api.aggstrawvn.repl.co/meme")
            data = await get.json()
            await ctx.send(data["result"])
async def setup(bot):
    await bot.add_cog(Meme(bot))