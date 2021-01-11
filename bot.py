import discord
import sys
import base64
bot = discord.Client()
token = sys.argv[1]
channel_id = int(sys.argv[2])
msg = sys.argv[3]
@bot.event
async def on_ready():
        channel = bot.get_channel(channel_id)
        await channel.send(base64.b64decode(msg).decode())
        await bot.close()

bot.run(token)
