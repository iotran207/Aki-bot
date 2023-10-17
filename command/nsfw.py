import aiohttp
from discord.ext import commands
import random
import json
import discord
class Nsfw(commands.Cog):
    config = {
        "name": "nsfw",
        "desc": "ảnh nsfw trên reddit=))",
        "use": "nsfw",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    @commands.is_nsfw()
    @commands.cooldown(3, 9, commands.BucketType.user)
    async def nsfw(self, ctx: commands.Context) -> None:
        await ctx.defer()
        try:
            result = []
            async with aiohttp.ClientSession() as session:
                get = await session.get("https://www.reddit.com/r/nsfw/new.json?sort=hot")
                data = await get.json()
                result = random.choice(data["data"]["children"])["data"]["url_overridden_by_dest"]
                image = await session.get(result)
                image = await image.read()
                if "redgifs" in result:
                    return await ctx.send(result.replace('watch', 'ifr'))
            await ctx.send(result)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Nsfw(bot))
