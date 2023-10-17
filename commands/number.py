import discord
from discord.ext import commands
import random
class Random(commands.Cog):
    config = {
        "name": "random",
        "desc": "Random một số từ 1 -> số bạn cần",
        "use": "random <number>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx, arg = None):
        if arg == None:
            await ctx.send('invalid argument')
        else:
            await ctx.send(str(random.randrange(1, int(arg)+1)))
async def setup(bot):
    await bot.add_cog(Random(bot))
