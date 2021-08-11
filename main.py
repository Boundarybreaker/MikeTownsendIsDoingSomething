# A discord bot that posts whenever Mike Townsend does something.
import asyncio
from multiprocessing import Process
from blaseball_mike import events
import discord
from os import path

loop = asyncio.get_event_loop()

client = discord.Client(loop=loop)

channels = []

@client.event
async def on_message(message):
    if message.content.lower().startswith("mike townsend (is here)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channels:
            channels.append(message.channel)
            save_config()
            await message.channel.send("Mike Townsend (is subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")
    elif message.content.lower().startswith("mike townsend (is gone)"):
        if message.author == client.user:
            return
        elif message.author.permissions_in(message.channel).manage_channels:
            channels.remove(message.channel)
            save_config()
            await message.channel.send("Mike Townsend (is no longer subscribed to this channel)")
        else:
            await message.channel.send("Mike Townsend (can only listen to members with Manage Channel permissions)")


@client.event
async def on_ready():
    if path.exists("channels.txt"):
        with open("channels.txt") as config:
            split = config.read().split("\n")
            for line in split:
                if line:
                    channel = await client.fetch_channel(int(line))
                    if channel not in channels:
                        channels.append(channel)


def save_config():
    with open("channels.txt", "w") as config:
        config.truncate(0)
        contents = ""
        for channel in channels:
            contents = contents + str(channel.id) + "\n"
        config.write(contents)


async def blaseball_loop():
    last_message = ""
    # update me to `https://www.blaseball.com/events/streamData` to get live feed!
    async for data in events.stream_events(url="https://api.sibr.dev/replay/v1/replay?from=2021-07-20T02:11:50-07:00"):
        if not data:
            continue
        if "games" in data:
            schedule = data["games"]["schedule"]
            for game in schedule:
                message = game["lastUpdate"]
                if message.lower().startswith("mike townsend") and message != last_message:
                    last_message = message
                    for channel in channels:
                        embed = discord.Embed()
                        embed.type = "rich"
                        embed.title = "Season " + str(data["games"]["sim"]["season"]) + ", day " + str(data["games"]["sim"]["season"]) + " - " + game["awayTeamNickname"] + " at " + game["homeTeamNickname"]
                        embed.description = "Mike Townsend (" + message[14:].replace(".", "") + ")"
                        embed.colour = int(game["awayTeamColor"].replace("#", "0x"), 16) if game["topOfInning"] else int(game["homeTeamColor"].replace("#", "0x"), 16)
                        await channel.send(embed=embed)


if __name__ == "__main__":
    loop.create_task(blaseball_loop())
    token = open("token.txt").read()
    client.run(token)
