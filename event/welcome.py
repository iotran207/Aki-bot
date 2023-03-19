from discord.ext import commands
from main import get_bank_data
import discord
class Welcome(commands.Cog):
    config = {
        "event": True
    }
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            data = await get_bank_data()
            check = data.get(str(member.guild.id))
            if check and check["welcome"].get("channel"):
                channel = self.bot.get_channel(data[str(member.guild.id)]["welcome"]["channel"])
                if check["welcome"].get("message"):
                    msg = check["welcome"]["message"]
                    em = discord.Embed(title="===***WELCOME***===", description=f'{msg}', color = 0xFFF)
                    await channel.send(f"**Chào mừng <@{member.id}> đã đến với server**",embed = em)
                    return
                await channel.send(f"**Chào mừng <@{member.id}> đã đến với server**")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Welcome(bot))
