import discord
from discord.ext import commands
import datetime
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

CATEGORY_ID = your
EXEMPT_USER_ID = your

DISCORD_KEYWORDS = ["discord.gg", "discord.com/invite"] 

BASE = "https://discord.com/api/v9/"
TOKEN = '' # <- your bot token 

def timeout_user(user_id: int, guild_id: int, duration: int):
    endpoint = f'guilds/{guild_id}/members/{user_id}'
    headers = {"Authorization": f"Bot {TOKEN}"}
    url = BASE + endpoint
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)).isoformat()
    json = {'communication_disabled_until': timeout}
    session = requests.patch(url, json=json, headers=headers)
    return session.status_code

@bot.event
async def on_ready():
    print('Banner Bot on')

@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.channel.category_id != CATEGORY_ID:
            if any(keyword in message.content.lower() for keyword in DISCORD_KEYWORDS):
                if message.author.id != EXEMPT_USER_ID:
                    await message.delete()
                    status = timeout_user(message.author.id, message.guild.id, 1)
                    if status in range(200, 299): # time out 1m
                        await message.channel.trigger_typing()
                        await message.channel.send(f"{message.author.mention}Unerlaubte Werbung ist strengstens untersagt.")

                        embed = discord.Embed(title="Warnung", description="Unerlaubte Werbung ist verboten.", color=0x96FF33) 
                        await message.author.send(embed=embed)

bot.run(TOKEN)