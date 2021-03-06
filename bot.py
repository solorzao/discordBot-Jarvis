# bot.py
import os
import random
import pandas
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! You can type "!help" at anytime in the server to pull up a list of things I can help you with it, enjoy your stay!'
    )


@bot.command(name='roast_me', help='Jarvis coming in hot to roast you.')
async def roast_initiated(ctx):
    if ctx.author == bot.user:
        return

    name = ctx.author.mention

    roasts = [
        f'{name} you\'re looking pretty rough this evening. You look like if sweatpants were a person.',
        f'{name} you\'re my favorite person besides every other person I\'ve ever met.',
        f'{name} I envy people who have never met you.',
        f'{name} if you were an inanimate object, you’d be a participation trophy.',
        f'{name} you are a pizza burn on the roof of the world\'s mouth.',
        f'{name} if genius skips a generation, your children will be brilliant.',
        f'{name} you have the charm and charisma of a burning orphanage.',
        f'{name} if there was a single intelligent thought in your head it would have died from loneliness.',
        f'{name} I want you to be the pallbearer at my funeral so you can let me down one last time.',
        f'{name} you are the human embodiment of an eight-dollar haircut.',
        f'{name} you\'re so inbred you\'re a sandwich.',
        f'{name} if I had a gun, with two bullets, and I was in a room with Hitler, Bin Laden and you, I would shoot you twice.'
    ]

    response = random.choice(roasts)
    await ctx.channel.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='random_number_range', help='Gives you back a random number in between your range.')
async def roll(ctx, number1: int, number2: int):
    if number1 < number2:
        response = random.randrange(number1, number2)
    elif number1 > number2:
        response = random.randrange(number2, number1)
    else:
        response = 'Error, does not compute, please try again with numbers that have a valid range.'

    await ctx.send(response)


@bot.command(name='hello', help='Sends greeting back.')
async def reply_greeting(ctx):
    if ctx.author == bot.user:
        return

    name = ctx.author.mention

    response = f'Hello {name}!'
    await ctx.send(response)

@bot.command(name='add_point', help='Adds channel point to user profile.')
async def add_point(ctx):
    entry = pandas.DataFrame(columns=['username', 'points'])

    entry = entry.append({'username': ctx.author,
                            'points': 1}, ignore_index=True)

    fileLocation = "channel_points.csv"
    entry.to_csv(fileLocation)

    name = ctx.author.mention

    response = f'{name} Succesfully added point!'
    await ctx.send(response)


bot.run(TOKEN)
