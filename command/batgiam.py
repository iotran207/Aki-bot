import discord
from discord.ext import commands
import aiohttp
import easy_pil
import aiofiles
import os
import asyncio
class Prison(commands.Cog):
    config = {
        "name": "batgiam",
        "desc": "cho ai đó vào biên chế nhà nước+)",
        "use": 'prison <@mention>',
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def batgiam(self, ctx, member: discord.Member = None):
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get("https://i.ibb.co/1MJ43Ds/ep1g-G3r-d.webp")
                get = await get.read()
                f = await aiofiles.open(os.path.dirname(__file__) + "/cache/prison.png", mode="wb")
                await f.write(get)
                await f.close()
                if member == None:
                    tag = f"<@{ctx.author.id}>"
                    image = await easy_pil.load_image_async(ctx.author.display_avatar.url)
                else:
                    tag = f"<@{member.id}>"
                    image = await easy_pil.load_image_async(member.display_avatar.url)
                back = easy_pil.Editor(os.path.dirname(__file__) + "/cache/prison.png")
                paste = easy_pil.Editor(image).circle_image()
                paste.resize((110, 110))
                back.paste(paste, (150, 85))
                file = discord.File(fp=back.image_bytes, filename='circle.png')
                await ctx.send(f"chúc mừng e đã vào biên chế nhà nước nhé=) {tag}",file = file)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Prison(bot))

            
