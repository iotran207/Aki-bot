import discord
from discord.ext import commands
from main import get_bank_data, open_account, save_member_data
import random
from commands.cache.list_color import list_color
import datetime
class Cfs(commands.Cog):
    config = {
        "name": "cfs",
        "desc": "viet confession an danh va cong khai gui den mot channel trong sever",
        "use": "cfs <set/write> <noi_dung>",
        'author': "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cfs(self, ctx, mode = None, *,content = None):
        await ctx.message.delete()
        try:
            if content == None or mode == None:
                return await ctx.send("sai cu phap")
            data = await get_bank_data()
            if mode == "set":
                if not ctx.author.guild_permissions.manage_channels:
                    return await ctx.send("ban phai co quyen quan li kenh de dat kenh confession")
                elif not content.isdigit():
                    return await ctx.send("ban phai nhap kem theo mot day so id channel muon de lam kenh confession")
                content = int(content)
                channel = self.bot.get_channel(content)
                await open_account(ctx.guild.id)
                data[f"{ctx.guild.id}"]["cfs"] = {}
                data[f"{ctx.guild.id}"]["cfs"]["channel"] = content
                data[f"{ctx.guild.id}"]["cfs"]["confession"] = 1
                save_member_data(data)
                await ctx.send(f"da chuyen kenh confession sang kenh <#{content}>")
                await channel.send("da chuyen kenh confession sang kenh nay <@ctx.author.id>")
            elif mode == "write":
                if not data[f"{ctx.guild.id}"].setdefault("cfs"):
                    return await ctx.send(" Bạn chưa thiết lập kênh confession cho bot")
                if not content:
                    return await ctx.send("hay nhap noi dung ban muon viet vao confession")
                channel = self.bot.get_channel(data[f"{ctx.guild.id}"]["cfs"]["channel"])
                cfs = data[f"{ctx.guild.id}"]["cfs"]["confession"]
                em = discord.Embed(title = f'**Confession✉️** (#{cfs})', description=f"_{content}_\n\n\nby:......", colour=random.choice(list_color))
                em.set_thumbnail(url="https://i.ibb.co/WVQt2r4/che-do-an-danh.png")
                em.set_footer(text= f'confession | {datetime.date.today().strftime("%d/%m/%Y")}')
                data[f"{ctx.guild.id}"]["cfs"]["confession"] += 1
                save_member_data(data)
                await channel.send(embed=em)
        except Exception as e:
            print(e)
            await ctx.send(f"error: {e}")
async def setup(bot):
    await bot.add_cog(Cfs(bot))