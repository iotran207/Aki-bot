import requests
from discord.ext import commands
import discord
class Ask(commands.Cog):
    config = {
      "name": "ask",
      "desc": "hỏi AI",
      "use": "ask <question>",
      "author": "Anh Duc(aki team)"
    }
    def init(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ask(self, ctx, *,question: str = None):
        try:
            await ctx.defer()
            api = "http://chatgpt-bi-ngu.camhcutkhongbaysieudeptrai.repl.co/ass"
            result = requests.post(api, data=question.encode()).text
            await ctx.reply(result)
        except Exception as e:
            await ctx.send(f"đã xảy ra lỗi:\n{e}")
async def setup(bot):
    await bot.add_cog(Ask(bot))