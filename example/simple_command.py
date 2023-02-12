from discord.ext import commands
import discord
import aiohttp
class Demo1(commands.Cog):
    config = {
        "name": "...",
        "desc": "...",
        "use": "...",
        "author": "...",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def say(self,ctx,*,content:str):
        await ctx.reply(content)
    


async def setup(bot):
    await bot.add_cog(Demo1(bot))
