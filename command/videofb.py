from discord.ext import commands
from discord import *
import io,aiohttp
class Videofb(commands.Cog):
    config = {
        "name": "videofb",
        "desc": "dowload video từ facebook",
        "use": "videofb <link video facebook>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def videofb(self, ctx,link_video_fb:str):
        load_msg = await ctx.reply("Đang thực hiện yêu cầu vui lòng đợi...")
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.nguyenmanh.name.vn/api/fbDL?url={link_video_fb}&apikey=I7IV8DHe"
                async with session.get(url) as get:
                    video_url_nowatermark = (await get.json())['result']["sd"]
                    print(url)
                async with session.get(f'{video_url_nowatermark}') as get2:
                    video = await get2.read()
                await load_msg.delete()
                if len(video) > 1e9: 
                    await ctx.reply(content='Video facebook quá dài không thể gửi', ephemeral=False)
                    return
        
                file = File(io.BytesIO(video), filename='video.mp4')
                await ctx.reply('Nếu không xem được video có thể là do link lỗi (hãy thử bấm vào xem video facebook và copy link có chữ "fb.watch" ở đầu sau đó thử lại lệnh bạn nhé', file=file)
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Videofb(bot))