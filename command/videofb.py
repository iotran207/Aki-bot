from discord.ext import commands
from discord import *
import io
import requests
class Videofb(commands.Cog):
    config = {
        "name": "videofb",
        "desc": "dowload video từ facebook",
        "use": "videofb <link video facebook>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def videofb(self, ctx,link_video_fb:str):
        await ctx.defer()
        load_msg = await ctx.reply("Đang thực hiện yêu cầu vui lòng đợi...")
        try:
            video = requests.get(requests.post('https://api.letuan.edu.vn', data=str(link_video_fb)).json()["link"]).content
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