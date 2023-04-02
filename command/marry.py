import json
from main import open_account, get_bank_data, save_member_data
from command.cache.list_color import list_color 
import random
import datetime
import discord
from discord.ext import commands
class Marry(commands.Cog):
    config = {
        "name": "marry",
        "desc": "lenh nay danh cho cac cap doi yeu nhau",
        "use": "marry @mention",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def marry(self, ctx, user: discord.Member):
        try:
            await open_account(user.id)
            await open_account(ctx.author.id)
            data = await get_bank_data()
            em = discord.Embed(title= f":church: <@{ctx.author.id}> **đã gửi lời cầu hôn tới** <@{user.id}>", description=f"**{user.name}, bạn có chấp nhận lời câu hôn của {ctx.author.name} hay không?**", color = random.choice(list_color))
            send = await ctx.send(embed=em)
            await send.add_reaction("❎")
            await send.add_reaction("✅")
            
            def check(reaction, mem):
                return mem == user and str(reaction.emoji) == '✅'
                
            react = await self.bot.wait_for("reaction_add", check = check)
            if react:
                await send.delete()
                data[f"{ctx.author.id}"]["dating"] = {}
                save_member_data(data)
                data[str(ctx.author.id)]["dating"]["ngayyeunhau"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S" )
                data[str(ctx.author.id)]["dating"]["friend_name"] = user.name
                data[str(ctx.author.id)]["dating"]["friend_avar"] = str(user.display_avatar.url)
                data[f"{user.id}"]["dating"] = {}
                save_member_data(data)
                data[str(user.id)]["dating"]["ngayyeunhau"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S" )
                data[str(user.id)]["dating"]["friend_name"] = ctx.author.name
                data[str(user.id)]["dating"]["friend_avar"] = str(ctx.author.display_avatar.url)
                save_member_data(data)
                await ctx.send(f":heart: **chúc mừng {ctx.author.name} và {user.name} đã về chung 1 nhà, hãy sử dụng lệnh dating để xem thông tin tình trạng của bạn với người ấy** :heart:")
            else:
                await send.delete()
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Marry(bot))
