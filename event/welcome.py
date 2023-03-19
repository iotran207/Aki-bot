from discord.ext import commands
from main import get_bank_data
import discord
import aiohttp
class Welcome(commands.Cog):
    config = {
        "event": True
    }
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            async with aiohttp.ClientSession() as session:
                get = await session.get(f"https://nekos.best/api/v2/cuddle?amount=1")
                data = await get.json()
                if get.status == 200:
                    gif = data["results"][0]["url"]
            data = await get_bank_data()
            check = data.get(str(member.guild.id))
            if check and check["welcome"].get("channel"):
                channel = self.bot.get_channel(data[str(member.guild.id)]["welcome"]["channel"])
                if check["welcome"].get("message"):
                    msg = check["welcome"]["message"]
                    em = discord.Embed(title="===***WELCOME***===", description=f'{msg.replace("<<member>>", f"<@{member.id}>")}', color = 0xFFF)
                    em.set_image(url = gif)
                    await channel.send(f"**Chào mừng <@{member.id}> đã đến với server**",embed = em)
                    return
                await channel.send(f"**Chào mừng <@{member.id}> đã đến với server**")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Welcome(bot))
