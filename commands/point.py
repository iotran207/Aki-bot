import discord
from discord.ext import commands
import easy_pil
import aiohttp
import aiofiles
class Point(commands.Cog):
    config = {
        "name": "point",
        "desc": "Mọi ng đều chỉ vào bạn=)",
        "use": "point <@member>",
        "author": " Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def point(self, ctx, member: discord.User=None):
        try:
            await ctx.defer()
            if not member:
                image = await easy_pil.load_image_async(ctx.author.display_avatar.url)
                back = await easy_pil.load_image_async("https://i.ibb.co/ZVsPx2k/memes-painting-hd-wallpaper-preview.jpg")
                avatar = easy_pil.Editor(image)
                background = easy_pil.Editor(back)
                avatar.circle_image()
                avatar.resize((100,100))
                background.paste(avatar, (320,130))
                file = discord.File(fp=background.image_bytes, filename="point.png")
                await ctx.interaction.followup.send(f"<@{ctx.message.author.id}>",file=file)
            else:
                image = await easy_pil.load_image_async(member.display_avatar.url)
                back = await easy_pil.load_image_async("https://i.ibb.co/ZVsPx2k/memes-painting-hd-wallpaper-preview.jpg")
                avatar = easy_pil.Editor(image)
                background = easy_pil.Editor(back)
                avatar.circle_image()
                avatar.resize((100,100))
                background.paste(avatar, (320,130))
                file = discord.File(fp=background.image_bytes, filename="point.png")
                await ctx.send(f"<@{member.id}>",file=file)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Point(bot))