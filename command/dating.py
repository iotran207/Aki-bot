import discord
from discord.ext import commands
from main import get_bank_data
import datetime
from command.cache.list_color import list_color 
import random
import json
import aiohttp
import easy_pil
class Dating(commands.Cog):
    config = {
        "name": "dating",
        "desc": "xem thong tin moi quan he cua ban voi nguoi ay",
        'use': "dating",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dating(self, ctx):
        try:
            data = await get_bank_data()
            if not data[f"{ctx.author.id}"].get("dating"):
                await ctx.reply("bạn chưa có mối quan hệ nào cả")
            else:
                async with ctx.typing():
                    image = easy_pil.Editor(await easy_pil.load_image_async("https://i.ibb.co/bzNSZYt/IMG-20230318-120207.jpg"))
                    avar1 = easy_pil.Editor(await easy_pil.load_image_async(str(ctx.author.display_avatar.url))).circle_image()
                    avar2 = easy_pil.Editor(await easy_pil.load_image_async(data[f"{ctx.author.id}"]["dating"]["friend_avar"])).circle_image()
                    avar1.resize((150,150))
                    avar2.resize((150,150))
                    image.paste(avar1, (43,107))
                    image.paste(avar2, (730,107))
                    async with aiohttp.ClientSession() as session:
                        url = "https://raw.githubusercontent.com/ledingg1997/ledingg-/main/datathinh.json"
                        get = await session.get(url)
                        get = json.loads(await get.text())
                        thinh = get["data"][f"{random.randint(1, 186)}"]
                    t = "\n"
                    path = data[f"{ctx.author.id}"]['dating']
                    em = discord.Embed(title= f"**:heart: [TRẠNG THÁI MỐI QUAN HỆ] :heart:**", description=f"**tên của bạn**: {ctx.author.name}**{t}tên người ấy**: {path['friend_name']}{t}**các bạn bắt đầu mối quan hệ ngày**: {path['ngayyeunhau']}{t}**các bạn đã yêu nhau được**: {datetime.datetime.now() - datetime.datetime.strptime(path['ngayyeunhau'], '%d/%m/%Y %H:%M:%S')}\n∆===================∆\n***{thinh}***", color = random.choice(list_color))
                    em.set_image(url = "attachment://dhbc.png")
                    
                    await ctx.send(embed=em,file=discord.File(image.image_bytes , filename="dhbc.png"))
        except Exception as e:
            await ctx.send(e)
async def setup(bot):
    await bot.add_cog(Dating(bot))
