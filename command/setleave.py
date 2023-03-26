import discord
from discord.ext import commands
import json
from main import get_bank_data, open_account, save_member_data
class Setleave(commands.Cog):
    config = {
        "name": "setleave",
        "desc": "cài đặt channel để gửi tin nhắn tạm biệt thành viên khi họ rời đi",
        "use": "setleave [message/channel] <messsage (dùng <<member>> thay cho tag thanh vien)/id_channel>",
        "author": 'Anh Duc(aki team)'
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def setleave(self, ctx,mode: str = None, *, channel = None):
        try:
            if not mode:
                await ctx.reply("sai cú pháp")
                return
            await open_account(ctx.message.guild.id)
            data = await get_bank_data()
            check = data[f"{ctx.message.guild.id}"]
            if mode == "channel":
                if check.get("leave"):
                    set = self.bot.get_channel(int(channel))
                    if set:
                        data[f"{ctx.message.guild.id}"]["leave"]["channel"] = int(channel)
                        save_member_data(data)
                        await set.send(f"<@{ctx.author.id}> đã chọn channel <#{channel}> mang id {channel} là kênh tạm biệt thành viên")
                if not check.get("leave"):
                    data[f"{ctx.message.guild.id}"]["leave"] = {}
                    data[f"{ctx.message.guild.id}"]["leave"]["channel"] = int(channel)
                    set = self.bot.get_channel(int(channel))
                    if set:
                        data[f"{ctx.message.guild.id}"]["leave"]["channel"] = int(channel)
                        save_member_data(data)
                        await set.send(f"<@{ctx.author.id}> đã chọn channel <#{channel}> mang id {channel} là kênh tạm biệt thành viên")
            elif mode == "message":
                if check.get("leave"):
                    msg = str(channel)
                    data[str(ctx.message.guild.id)]["leave"]["message"] = msg
                    save_member_data(data)
                    await ctx.reply("đã đặt thành công tin nhắn tam biet thành viên")
                elif not check.get("leave"):
                    msg = str(channel)
                    data[str(ctx.message.guild.id)]["leave"] = {}
                    data[str(ctx.message.guild.id)]["leave"]["message"] = msg
                    save_member_data(data)
                    await ctx.reply("đã đặt thành công tin nhắn tam biet thành viên")
        except Exception as e:
            await ctx.send(e)
async def setup(bot):
    await bot.add_cog(Setleave(bot))
