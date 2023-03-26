from discord.ext import commands
from main import get_bank_data
import discord
import aiohttp
class Leave(commands.Cog):
    config = {
        "event": True
    }
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_member_remove(self,payload):
        try:
            data = await get_bank_data()
            check = data.get(f"{payload.guild_id}")
            if check and check["leave"].get("channel"):
                async with aiohttp.ClientSession() as session:
                    get = await session.get(f"https://nekos.best/api/v2/cry?amount=1")
                    data = await get.json()
                    if get.status == 200:
                        gif = data["results"][0]["url"]
                data = await get_bank_data()
                channel = self.bot.get_channel(data[f"{payload.guild_id}"]["leave"]["channel"])
                if check["leave"].get("message"):
                    msg = check["leave"]["message"]
                    em = discord.Embed(title="===***GOODBYE***===", description=f'{msg.replace("<<member>>", f"<@{payload.user.id}>")}', color = 0xFFF)
                    em.set_image(url = gif)
                    await channel.send(f"**Tam biet <@{payload.user.id}> **",embed = em)
                    return
                await channel.send(f"**Tạm biệt <@{payload.user.id}> **")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Leave(bot))
