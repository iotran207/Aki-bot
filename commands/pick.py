import random
import discord
from discord.ext import commands
from commands.cache.list_color import list_color
class Pick(commands.Cog):
    config = {
        "name": "pick",
        "desc": "bot se chon 1 trong 2 cai ma ban dua",
        "use": "pick <luachon1>, <luachon2>,...",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def pick(self, ctx, *, pick: str):
        try:
            await ctx.reply(f":game_die: **{ctx.author.name}**, Tôi chọn " + random.choice(pick.split(",")) + " :game_die:")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Pick(bot))
