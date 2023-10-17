from discord.ext import commands
class Ping(commands.Cog):
    config = {
        "name": "ping",
        "desc": "kiểm tra độ trễ của bot",
        "use": "ping",
        "author": "King."
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    async def ping(self,ctx):
        try:
            await ctx.reply(f"Ping: `{self.bot.latency * 1000 :.2f}` ms", ephemeral = True)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Ping(bot))