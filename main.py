import os

import discord
from discord.ext import commands
from pathlib import Path
import sqlite3
import math
from dotenv import load_dotenv
from datetime import datetime
from humanize_date import humanize_date

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='?')

if not Path('dramalist.db').exists():
    Path('dramalist.db').touch()

conn = sqlite3.connect('dramalist.db')
curr = conn.cursor()

@bot.event
async def on_ready():
    print('%s has connected to Discord!' % bot.user.name)


@bot.command(name='list', help='Lists all the k-dramas currently being watched in the server')
async def list_shows(ctx, page=1):
    fetch_size = 5
    count = curr.execute('SELECT COUNT(*) FROM drama').fetchone()[0]
    footer = "%d of %d" % (page, int(math.ceil(count/fetch_size)))
    desc = []
    for row in curr.execute('SELECT * FROM drama LIMIT ?,?', (str((page-1)*fetch_size), str(fetch_size))):
        desc.append("[%s](%s) Episode %s" % (row[0], row[2], row[1]))

    embed = discord.Embed(title="Currently watched shows", color=0xFF5733, description="\n".join(desc))
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


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
async def add_show(ctx, name: str, url: str = ""):
    curr.execute("INSERT INTO drama(name,url) VALUES (?,?)", (name.title(), url))
    conn.commit()
    await ctx.send("Added %s to the list of shows" % name.title())


@bot.command(name="drop", help="Drop a show")
async def drop_show(ctx, name):
    curr.execute("DELETE FROM drama WHERE name = ?", (name.title(), ))
    conn.commit()
    await ctx.send("No longer watching %s" % name.title())


@bot.command(name="test-when", help="Shows the next stream of a certain show")
async def when_next_show(ctx, show_name: str):
    watch_time = curr.execute("SELECT time from watch_times where name = ?", (show_name.title(),)).fetchone()
    if watch_time is None:
        await ctx.send("There's no plans to watch %s right, we should book one" % show_name.title())
        return

    time = datetime.strptime(watch_time[0], '%Y-%m-%d %H:%M:%S')
    if time < datetime.now():
        await ctx.send("Aww we already watched %s %s" % (show_name.title(), humanize_date(time)))
    else:
        await ctx.send("We'll be watching %s %s" % (show_name.title(), humanize_date(time)))


@bot.command(name="test-next", help="Set when to watch next episode")
async def set_next_show(ctx, show_name: str, next_time: str):
    if curr.execute("SELECT COUNT(*) from watch_times WHERE name = ?", (show_name.title(),)).fetchone()[0] > 0:
        curr.execute("UPDATE watch_times SET time = datetime(?) WHERE name = ?", (next_time, show_name.title(),))
        conn.commit()
    else:
        curr.execute("INSERT into watch_times(name, time) VALUES (?,datetime(?))", (show_name.title(), next_time,))
    conn.commit()
    await ctx.send("Okay! We'll watch %s at %s" % (show_name.title(), next_time))

bot.run(os.getenv('TOKEN'))
