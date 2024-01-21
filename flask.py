import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Add your custom logic here for handling messages
    await bot.process_commands(message)

@bot.command(name='hello')
async def hello(ctx):
    # Command example: !hello
    await ctx.send('Hello!')

# Moderation Commands
@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason=None):
    # Command example: !ban @user Reason
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned. Reason: {reason}')

@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason=None):
    # Command example: !kick @user Reason
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked. Reason: {reason}')

@bot.command(name='mute')
async def mute(ctx, member: discord.Member, *, reason=None):
    # Command example: !mute @user Reason
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not mute_role:
        await ctx.send('Mute role not found. Use `!create_mute_role` to create it.')
        return

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} has been muted. Reason: {reason}')

@bot.command(name='create_mute_role')
async def create_mute_role(ctx):
    # Command example: !create_mute_role
    mute_permissions = discord.Permissions(send_messages=False, speak=False)
    mute_role = await ctx.guild.create_role(name='Muted', permissions=mute_permissions)

    for channel in ctx.guild.channels:
        await channel.set_permissions(mute_role, send_messages=False, speak=False)

    await ctx.send('Mute role created successfully.')

import os

# Add more commands or event handlers as needed
TOKEN = os.gentenv("TOKEN")
bot.run(TOKEN)
