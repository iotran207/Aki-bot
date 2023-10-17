from discord.ext import commands
import discord 
from main import config
class Send_file(commands.Cog):
    config = {
        "name": "send_file", 
        "desc": "gui file trong bot",
        "use": "send_file <path/to/file>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def send_file(self, ctx,file_name):
        try:
            if str(ctx.author.id) not in [str(config["admin_id"])]:
                await ctx.send("ban khong phai admin=))")
            else:
                await ctx.reply(file=discord.File(fp=f'{file_name}'))
        except Exception as e:
            print(e)
            await ctx.send("file name error")
async def setup(bot):
    await bot.add_cog(Send_file(bot))
