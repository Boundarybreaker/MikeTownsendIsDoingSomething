# A discord bot that posts whenever Mike Townsend does something.
from blaseball_mike import events
import discord

client = discord.Client()

with open("token.txt") as token:
    client.run(token.read())

channels = []

@client.event
async def on_message(message):
    if message.content.lower().startswith("mike townsend (is here)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channel:
            channels.add(message.channel)
            await message.channel.send("Mike Townsend (is subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")
    elif message.content.lower().startswith("mike townsend (is gone)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channel:
            channels.remove(message.channel)
            await message.channel.send("Mike Townsend (is no longer subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")


# TODO: formatting, info about game/day, messages that don't start with townsend, etc.
# TODO: does this actually work? can't check because Mike Townsend (will not be playing until the next On Season)
for data in await events.stream_events():
    schedule = data.value.games.schedule
    for game in schedule:
        message = game.lastUpdate
        if message.lower().startswith("mike townsend"):
            for channel in channels:
                channel.send("Mike Townsend (" + message[14:] + ")")

