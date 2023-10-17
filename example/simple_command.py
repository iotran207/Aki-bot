from discord.ext import commands
import discord
import aiohttp
class Say(commands.Cog): 
    config = {
        "name": "say", # ten command
        "desc": "de bot nhan dieu ban muon nhan", #mo ta ve command(dung de lam gi?)
        "use": "say <content>", #cach dung (neu khong can dung argument thi ghi me lai ten lenh la dc)
        "author": "king(aki team)",
        "event": False
    }
    def __init__(self, bot):
        self.bot = bot
    #@commands.Cog.listener() nhan cac event (doc docs cua discord.py de hieu ro hon=)))
    @commands.hybrid_command() #Bao gồm cả prefix command và slash command hoặc sử dụng commands.command() chỉ bao gồm prefix command
    async def say(self,ctx,*,content:str):
        await ctx.reply(content)
async def setup(bot):
    await bot.add_cog(Say(bot))
