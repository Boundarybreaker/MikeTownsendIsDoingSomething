# A discord bot that posts whenever Mike Townsend does something.
import asyncio
from multiprocessing import Process
from blaseball_mike import events
import discord

client = discord.Client()

# FIXME: this doesn't sync between threads, and I have no idea how to make it do that!
channels = []


@client.event
async def on_message(message):
    if message.content.lower().startswith("mike townsend (is here)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channels:
            channels.append(message.channel)
            await message.channel.send("Mike Townsend (is subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")
    elif message.content.lower().startswith("mike townsend (is gone)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channels:
            channels.remove(message.channel)
            await message.channel.send("Mike Townsend (is no longer subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")


async def blaseball_loop():
    last_message = ""
    # TODO: formatting, info about game/day, messages that don't start with townsend, etc.
    async for data in events.stream_events(url="https://www.blaseball.com/events/streamData"):
        if "games" in data:
            schedule = data["games"]["schedule"]
            for game in schedule:
                if game["awayTeamName"] == "Seattle Garages" or game["homeTeamName"] == "Seattle Garages":
                    message = game["lastUpdate"]
                    if message.lower().startswith("mike townsend") and message != last_message:
                        last_message = message
                        for channel in channels:
                            await channel.send("Mike Townsend (" + message[14:] + ")")


def blaseball_main():
    asyncio.run(blaseball_loop())


def discord_main():
    token = open("token.txt").read()
    client.run(token)


if __name__ == "__main__":
    Process(target=blaseball_main).start()
    Process(target=discord_main).start()
