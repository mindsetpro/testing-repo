import discord
from discord.ext import commands
from flask import Flask, render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session
import threading
import asyncio
import os

import secrets

# Generate a secure random key
secret_key = secrets.token_hex(16)

print(secret_key)


# Flask App
app = Flask(__name__)
app.secret_key = ''  # Replace with a secure secret key
discord = DiscordOAuth2Session(app)

# Discord Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Placeholder for bot settings (replace with actual persistence mechanism)
bot_settings = {
    'prefix': '!',
    'welcome_message': 'Welcome to the server!',
    'goodbye_message': 'Goodbye!',
    'embed_channel': 1234567890,  # Default embed channel ID
}

@app.route('/')
def home():
    if not discord.authorized:
        return redirect(url_for('login'))
    user = discord.fetch_user()
    return render_template('home.html', user=user, settings=bot_settings)

@app.route('/update_settings', methods=['POST'])
def update_settings():
    if not discord.authorized:
        return redirect(url_for('login'))

    prefix = request.form.get('prefix')
    welcome_message = request.form.get('welcome_message')
    goodbye_message = request.form.get('goodbye_message')
    embed_channel = int(request.form.get('embed_channel'))

    # Update bot settings (replace with actual persistence mechanism)
    bot_settings['prefix'] = prefix
    bot_settings['welcome_message'] = welcome_message
    bot_settings['goodbye_message'] = goodbye_message
    bot_settings['embed_channel'] = embed_channel

    # Create an embed to display the updated settings
    embed = discord.Embed(
        title='Bot Settings Updated',
        description=f'Prefix: {prefix}\nWelcome Message: {welcome_message}\nGoodbye Message: {goodbye_message}\nEmbed Channel: <#{embed_channel}>',
        color=discord.Color.green()
    )

    # Replace with the actual channel ID where you want to send the embed
    channel_id = embed_channel
    channel = bot.get_channel(channel_id)
    asyncio.ensure_future(channel.send(embed=embed))

    return redirect(url_for('home'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='ban')
async def ban(ctx, member: discord.Member):
    await ctx.send(f'{member.mention} has been banned.')

if __name__ == '__main__':
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'threaded': True})
    bot_thread = threading.Thread(target=bot.run, kwargs={'token': os.getenv("TOKEN")}

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()
