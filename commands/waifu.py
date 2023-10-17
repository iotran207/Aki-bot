import discord
from discord.ext import commands
import aiohttp
import json
import random
from commands.cache.list_color import list_color
class Waifu(commands.Cog):
  config = {
      "name": "waifu",
      "desc": "ảnh waifu+))",
      "use": "waifu",
      "author": "Anh Duc(aki team)"
    }
  def __init__(self, bot):
    self.bot = bot
  @commands.hybrid_command()
  @commands.cooldown(1, 4, commands.BucketType.user)
  async def waifu(self, ctx):
    await ctx.defer()
    try:
        async with aiohttp.ClientSession() as session:
            get = await session.get(f"https://nekos.best/api/v2/waifu?amount=1")
            data = await get.json()
            if get.status == 200:
                gif = data["results"][0]["url"]
                em_load = discord.Embed(colour = random.choice(list_color))
                em_load.set_image(url = gif)
                await ctx.reply(embed = em_load)
                return
            await ctx.send("error")
    except Exception as e:
      print(e)
async def setup(bot):
  await bot.add_cog(Waifu(bot))
