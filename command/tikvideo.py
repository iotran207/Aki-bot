from discord.ext import commands
from discord import *
import io,aiohttp
class Tikvideo(commands.Cog):
    config = {
        "name": "tikvideo",
        "desc": "dowload video từ tiktok",
        "use": "tikvideo <link video tiktok>",
        "author": "King.(maku team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def tikvideo(self, ctx,link_video_tiktok:str):
        load_msg = await ctx.reply("Đang thực hiện yêu cầu vui lòng đợi...")
        try:
            async with aiohttp.ClientSession() as session:
                url = f'https://www.nguyenmanh.name.vn/api/tikDL?url={link_video_tiktok}&apikey=3AHlbNbA'
                async with session.get(url) as get:
                    video_url_nowatermark = (await get.json())['result']["video"]["nowatermark"]
                    print(url)
                async with session.get(f'{video_url_nowatermark}') as get2:
                    video = await get2.read()
                await load_msg.delete()
                if len(video) > 1e9: 
                    await ctx.reply(content='Video tiktok quá dài không thể gửi!', ephemeral=False)
                    return
        
                file = File(io.BytesIO(video), filename='video.mp4')
                await ctx.reply(file=file)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Tikvideo(bot))
