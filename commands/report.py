from discord.ext import commands
import discord
from main import config
from commands.cache.list_color import list_color
import random
class Report(commands.Cog):
    config = {
        "name": "report",
        "desc": "báo cáo bất cứ cái gì đến admin=)",
        "use": "report <content>",
        "author": "Anh Duc"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def report(self, ctx, *, content: str):
        try:
            admin =  [716146182849560598, config["admin_id"], 1014470866903511091]
            error = 0
            for i in admin:
                try:
                    send = await self.bot.fetch_user(i)
                    em = discord.Embed(title=f"**Báo cáo từ {ctx.author.name}**", description = f"Nội dung: _{content}_", color=random.choice(list_color))
                    em.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
                    await send.send(embed = em)
                except Exception as e:
                    error += 1
                    await ctx.send("đã xảy ra lỗi" + str(e))
                    continue
            await ctx.send(f"gửi báo cáo thành công đến {len(admin) - error} admin\nGửi báo cáo thất bại đến {error}")
        except Exception as e:
            print(e)
            await ctx.send(f"{e}")
async def setup(bot):
    await bot.add_cog(Report(bot))
        
