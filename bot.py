# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    roasts = [
        f'A little known fact is that a long time ago @{message.author.name} used to work at McDonald’s. It was the last time anyone said about your work, “I’m lovin’ it.”',
        f'We are doing this roast tonight to help @{message.author.name} live out one of his sexual fantasies, to have a room full of his friends shit all over him.',
        f'It’s nice to see such a diverse crowd here today. We’ve got Indians, Jews, Whites, and whatever the fuck @{message.author.name} is.', 
        f'@{message.author.name} you’re looking pretty rough this evening. @{message.author.name} looks like if sweatpants were a person.', 
        f'@{message.author.name} if laughter is the best medicine, your face must be curing the world.'
    ]

    if message.content == 'roast me!':
        response = random.choice(roasts)
        await message.channel.send(response)

    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)
