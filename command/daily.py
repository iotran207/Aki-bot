import discord
from discord.ext import commands
import random
from command.cache.list_color import list_color
class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 86400, type=commands.BucketType.user)
    async def daily(self, ctx):
        try:
            earn = random.randint(100, 200)
            self.bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {earn} WHERE user_id={ctx.author.id}')
            self.bot.database.commit()
            await ctx.send(f"bạn nhận được {earn}$ tiền thường hằng ngày")
        except Exception as e:
            await ctx.send(e)
    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"bạn chỉ được nhận thưởng hằng ngày mỗi 24h", color=random.choice(list_color))
            await ctx.send(embed=em)
async def setup(bot):
    await bot.add_cog(Daily(bot))
