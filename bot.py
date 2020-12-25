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

    name = message.author.name

    roasts = [
        f'It’s nice to see such a diverse crowd here today. We’ve got Indians, Jews, Whites, and whatever the fuck @{name} is.', 
        f'@{name} you\'re looking pretty rough this evening. @{name} looks like if sweatpants were a person.', 
        f'@{name} you\'re my favorite person besides every other person I\'ve ever met.', 
        f'@{name} I envy people who have never met you.', 
        f'@{name} if you were an inanimate object, you’d be a participation trophy.', 
        f'@{name} you are a pizza burn on the roof of the world\'s mouth.',
        f'@{name} if genius skips a generation, your children will be brilliant.',
        f'@{name} you have the charm and charisma of a burning orphanage.',
        f'@{name} if there was a single intelligent thought in your head it would have died from loneliness.',
        f'@{name} I want you to be the pallbearer at my funeral so you can let me down one last time.',
        f'@{name} you are the human embodiment of an eight-dollar haircut.',
        f'@{name} you\'re so inbred you\'re a sandwich.',
        f'If I had a gun, with two bullets, and I was in a room with Hitler, Bin Laden and @{name}, I would shoot @{name} twice.'
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
