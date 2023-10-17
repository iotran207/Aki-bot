import discord
from discord.ext import commands
import easy_pil
import aiofiles
import aiohttp
import os 
class Tromcho(commands.Cog):
    config = {
        "name": "tromcho",
        "desc": "chế ảnh xàm thôi:)",
        "use": "tromcho @mention",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def tromcho(self, ctx, arg: discord.User = None):
        await ctx.defer()
        if arg == None:
            await ctx.send('sai cu phap')
            return
        try:
            image = await easy_pil.load_image_async(ctx.message.author.display_avatar.url)
            image2 = await easy_pil.load_image_async(arg.display_avatar.url)
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://i.ibb.co/bgz3FYt/trom-cho-bi-xu-phat-the-nao-1811142901.jpg') as resp:
                    f = await aiofiles.open(os.path.dirname(__file__) + "/cache/" + 'tromcho_background.jpg', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
            back = easy_pil.Editor(os.path.dirname(__file__)+'/cache/tromcho_background.jpg')
            paste = easy_pil.Editor(image).circle_image()
            paste2 = easy_pil.Editor(image2).circle_image()
            paste2.resize((42, 42))
            paste.resize((40, 40))
            back.paste(paste, (279, 35))
            back.paste(paste2, (210, 200))
            await ctx.send(f't xich m lai bay gio:smiling_imp: :smiling_imp:{arg.mention}', file = discord.File(back.image_bytes, filename='circle.png'),ephemeral=True)
        except Exception as e:
            print(e)
            await ctx.send('error')
async def setup(bot):
    await bot.add_cog(Tromcho(bot))
