import discord
from discord.ext import commands
import json
from main import get_bank_data, open_account, save_member_data
class Setwelcome(commands.Cog):
    config = {
        "name": "setwelcome",
        "desc": "chọn và cài đặt channel để bot gửi tin nhắn chào mừng thành viên mới",
        "use": "setwelcome [message/channel] <messsage (dùng <<member>> thay cho tag thanh vien)/id_channel>",
        "author": 'Anh Duc(aki team)'
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def setwelcome(self, ctx, mode: str, *, channel):
        try:
            await open_account(ctx.message.guild.id)
            data = await get_bank_data()
            check = data[f"{ctx.message.guild.id}"].get("welcome")
            if mode == "channel" and check:
                set = self.bot.get_channel(int(channel))
                if set:
                    data[f"{ctx.message.guild.id}"]["welcome"]["channel"] = int(channel)
                    save_member_data(data)
                    await set.send(f"<@{ctx.author.id}> đã chọn channel <#{channel}> mang id {channel} là kênh chào mừng thành viên mới")
            elif mode == "message" and check:
                msg = str(channel)
                data[str(ctx.message.guild.id)]["welcome"]["message"] = msg.replace("<<member>>", f"<@{member.id}>")
                save_member_data(data)
                await ctx.reply("đã đặt thành công tin nhắn chào mừng thành viên mới")
        except Exception as e:
            await ctx.send(e)
async def setup(bot):
    await bot.add_cog(Setwelcome(bot))
