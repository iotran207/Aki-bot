import discord
from discord.ext import commands
import aiohttp
import json
class Imgtosketch(commands.Cog):
    config = {
        "name": "imgtosketch",
        "desc": "convert image to painting",
        "use": "imgtosketch {gui kem voi anh=)}",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def imgtosketch(self, ctx):
        try:
            await ctx.send("Vui lòng đợi trong vài giây, đang tải ảnh.....")
            msg = "chuyển đổi ảnh thành công"
            if ctx.message.attachments:
                for i in ctx.message.attachments:
                    async with aiohttp.ClientSession() as session:
                        a = await session.get(f"https://opencv-tutorial.aggstrawvn.repl.co/imgtosketch?url={i.url}&key=aki-bot")
                        if a.status == 200:
                            a = json.loads(await a.text())
                            for i in range(1,6):
                                msg += (f'\nlink: {a["img" + str(i)]}')
                        else:
                            await ctx.send('Error: Upload ảnh thất bại')
                await ctx.send(msg)
                return
            await ctx.send("Hãy gửi kèm theo các bức ảnh bạn muốn đăng lên")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Imgtosketch(bot))
