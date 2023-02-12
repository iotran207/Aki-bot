import datetime
import discord
from discord.ext import commands
import random 
from command.cache.list_color import list_color 
class Age(commands.Cog):
    config = {
      "name": "age",
      "desc": " tinh tuoi",
      "use": "age <day>/<month>/<year>",
      "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def age(self, ctx, age: str = None):
        if age == None:
            await ctx.send("bạn chưa nhập ngày tháng năm sinh của mình")
        else:
            try:
                age = age.split("/")   
                d1 = datetime.datetime(int(age[2]), int(age[1]), int(age[0]))
                time1 = str(datetime.datetime.now() - d1).split(",")[1]
                time2 = str(datetime.datetime.now() - d1).split(",")[0]
                time = int(time2.strip("days"))
                msg = f'{str(time//365)} tuổi, {str(time%365//30)} tháng, {str(time%365%30)} ngày, {time1[:-7].replace(":", " giờ ", 1).replace(":", " phút ") + " giây"}'
                em = discord.Embed(title="**Số tuổi của bạn hiện giờ là:**", description=f'{msg}', color = random.choice(list_color))
                await ctx.send(embed = em)
            except Exception as e:
                await ctx.send(f"đã xảy ra lỗi:\n{e}\n hãy sử dụng lệnh như sau\n<prefix>age <ngày>/<tháng>/<năm>")
async def setup(bot):
    await bot.add_cog(Age(bot))
