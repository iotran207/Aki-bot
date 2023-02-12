import aiohttp
import asyncio
import discord
from discord.ext import commands
class Pastebin(commands.Cog):
  config = {
    "name": "pastebin",
    "desc": "lưu tất cả lên pastebin:))",
    "use": "pastebin <text>",
    "author": "Anh Duc(aki team)"
  }
  def __init__(self, bot):
      self.bot = bot
  @commands.command()
  async def pastebin(self, ctx, *, text = None):
    if text == None:
      await ctx.send("bạn chưa nhập điều muốn bỏ vào ghi chú pastebin")
      return
    data = {
      "api_dev_key": "kyigdu9KrzQ3dUCuhIOzZQmr6btik5Fm",
      "api_paste_code": str(text),
      "api_option":"paste"
    }
    async with aiohttp.ClientSession() as session:
      get = await session.post("https://pastebin.com/api/api_post.php", data = data)
      link = await get.text()
      await ctx.send(f"link: {link}")
async def setup(bot):
  await bot.add_cog(Pastebin(bot))
