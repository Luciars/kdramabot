import os
import requests

import discord
from discord.ext import commands
from pathlib import Path
import sqlite3
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='?')

if not Path('dramalist.db').exists():
    Path('dramalist.db').touch()

conn = sqlite3.connect('dramalist.db')
curr = conn.cursor()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='list', help='Lists all the k-dramas currently being watched in the server')
async def list_shows(ctx):
    await ctx.send('Listing shows:')
    for row in curr.execute('SELECT * FROM drama'):
        await ctx.send('%s: Episode %s' % (row[0], row[1]))


@bot.command(name='update', help='Updates the show to the specified episode')
async def update_show(ctx, name, episode):
    curr.execute("UPDATE drama SET episode = ? WHERE name = ?", (episode, name.title()))
    conn.commit()
    await ctx.send("I've updated %s to episode %s" % (name, episode))

@bot.command(name='episode', help='Shows which episode of the current drama the server is on')
async def show_episode(ctx, name):
    curr.execute('SELECT episode FROM drama WHERE name = ?', (name.title(),))
    episode = curr.fetchone()[0]
    await ctx.send("We're currently on episode %s" % episode)

@bot.command(name='add', help='Adds show to list of shows user is currently watching')
async def add_show(ctx, name: str, episode: int):
    curr.execute("INSERT INTO drama VALUES (?,?,?)", (name.title(), episode))
    conn.commit()
    await ctx.send("Added %s to the list of shows" % name.title())

@bot.command(name="drop", help="Drop a show")
async def drop_show(ctx, name):
    curr.execute("DELETE FROM drama WHERE name = ?", (name.title(), ))
    conn.commit()
    await ctx.send("No longer watching %s" % name.title())

@bot.command(name="when", help="Shows the next stream of a certain show")
async def when_next_show(ctx):
    pass

@bot.command(name="url")
async def give_url(ctx, url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    html_doc = requests.get(url, headers=headers).content.decode()
    soup = BeautifulSoup(html_doc, 'html.parser')

@bot.command(name="test")
async def when_next_show(ctx, args, n: int):
    #date, time = curr.execute("SELECT date, time FROM stream WHERE name = ?", (name,))
    print(args)
    print(n)

bot.run(os.getenv('TOKEN'))
