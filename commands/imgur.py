import discord
from discord.ext import commands
import aiohttp
class Imgur(commands.Cog):
    config = {
        "name": "upimg",
        "desc": "upload image",
        "use": "upimg",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def upimg(self, ctx):
        if ctx.message.attachments:
            for i in ctx.message.attachments:
                async with aiohttp.ClientSession() as session:
                    a = await session.post(url="https://0x0.st", data={"url": f"{i.url}"})
                    
                    if a.status == 200:
                        a = await a.text()
                        await ctx.reply(f"upload ảnh thành công\nlink: {a}")
                    else:
                        await ctx.send('Error: Upload ảnh thất bại')
            return
        await ctx.send("Hãy gửi kèm theo các bức ảnh bạn muốn đăng lên")
async def setup(bot):
    await bot.add_cog(Imgur(bot))
