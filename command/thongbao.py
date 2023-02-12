from discord.ext import commands
import discord
from command.cache.list_color import list_color
import random
class Thongbao(commands.Cog):
    config = {
        "name": "thongbao",
        "desc": "gửi thông báo bằng embed đến 1 kênh của server",
        "use": "thongbao",
        "author": "King.",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def thongbao(self,ctx):
        try:
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            await ctx.send('cậu muốn tiêu đề là gì? 📰')
            title = await self.bot.wait_for('message', check=check)
        
            await ctx.send('cậu muốn nội dung của tin nhắn là gì? 💬')
            desc = await self.bot.wait_for('message', check=check)

            await ctx.send('Nhập id channel cậu muốn gửi đến? 📻 (Gửi thêm ảnh nếu bạn muốn có ảnh trong embed thông báo)')
            channelID1 = await self.bot.wait_for('message',check=check)
            channel_id = int(channelID1.content)
            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(title=title.content, description=desc.content, color=random.choice(list_color))
            img = channelID1.attachments
            if img:
                for i in img:
                    embed.set_image(url=str(i.url))
            await channel.send(embed=embed)
        except Exception as e:
            print(e)
    @thongbao.error
    async def thongbao_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send("bạn phải là admin mới có thể sử dụng lệnh")


async def setup(bot):
    await bot.add_cog(Thongbao(bot))
