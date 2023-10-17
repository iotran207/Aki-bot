import discord
from discord.ext import commands
import json
import aiohttp
import time
import io
class Weather(commands.Cog):
    config = {
        "name": "weather",
        "desc": "Xem dự báo thời tiết:)",
        "use": "weather <location>",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def weather(self, ctx, *, location: str = None):
        await ctx.defer()
        try:
            def f_to_c(f: int):
                return round((f - 32)/1.8)
            def time1(localtime: int):
                return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(localtime))
            url = f"https://api.accuweather.com/locations/v1/cities/search.json?q={location}&apikey=d7e795ae6a0d44aaa8abb1a0a7ac19e4&language=vi-vn"
            async with aiohttp.ClientSession() as session:
                image = await session.get(f"https://wttr.in/{location}.png?lang=vi")
                image = await image.read()
                
                search = await session.get(url)
                search = json.loads(await search.text())[0]["Key"]
                weather = await session.get(f"http://api.accuweather.com/forecasts/v1/daily/10day/{search}?apikey=d7e795ae6a0d44aaa8abb1a0a7ac19e4&details=true&language=vi")
                weather = json.loads(await weather.text())
                print(weather)
                forecast = weather["DailyForecasts"][0]
                headline = weather["Headline"]["Text"]
                sun_rise = time1(forecast["Sun"]["EpochRise"])
                sun_set = time1(forecast["Sun"]["EpochSet"])
                moon_rise = time1(forecast["Moon"]["EpochRise"])
                moon_set = time1(forecast["Moon"]["EpochSet"])
                max_temp = f_to_c(forecast["Temperature"]["Maximum"]["Value"])
                min_temp = f_to_c(forecast["Temperature"]["Minimum"]["Value"])
                feel_temp = f_to_c((forecast["RealFeelTemperature"]["Minimum"]["Value"] + forecast["RealFeelTemperature"]["Maximum"]["Value"])/2)
                wind_speed = round((int(forecast["Day"]["Wind"]["Speed"]["Value"]) + int(forecast["Day"]["Wind"]["Speed"]["Value"]))/2 * 1.609344)
                day = forecast["Day"]["LongPhrase"]
                night = forecast["Night"]["LongPhrase"]
                em = discord.Embed(title = "**===Weather===**", description=f"thời tiết: {headline}")
                em.add_field(name = "**Nhiệt độ cao nhất**", value=  f"{max_temp}°C")
                em.add_field(name = "**Nhiệt độ thấp nhất**", value= f"{min_temp}°C")
                em.add_field(name = "**Nhiệt độ trung bình cảm nhận được**", value = f"{feel_temp}°C")
                em.add_field(name = "**Tốc độ gió**", value = f"{wind_speed} km/h")
                em.add_field(name = "**Mặt trời mọc**", value = f"{sun_rise}")
                em.add_field(name = "**Mặt trời lặn**", value = f"{sun_set}")
                em.add_field(name = "**Mặt trăng mọc**", value = f"{moon_rise}")
                em.add_field(name = f"**Mặt trăng lặn**", value = f"{moon_set}")
                file = discord.File(io.BytesIO(image), filename = "weather.png")
                em.set_image(url = "attachment://weather.png")
                await ctx.send(embed = em, file = file)
                
        except Exception as e:
            print(e)
            await ctx.send("error, Địa điểm không tồn tại hoặc không có trong dữ liệu bot")
async def setup(bot):
            await bot.add_cog(Weather(bot))
