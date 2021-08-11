# Mike Townsend (is doing something)

A discord bot that posts whenever Blaseball player Mike Townsend does something.

Currently unfinished.

## To run:
- Download this project.
- Install `discord.py` and `blaseball_mike` via `pip`.
- Create a text file `token.txt` in the same directory as `main.py` and paste your discord bot token in.
- Run the file.
- Say `Mike Townsend (is here)` to subscribe to the bot in the current channel. Case insensitive.
- Say `Mike Townsend (is gone)` to unsubscribe from the bot in the current channel. Case insensitive.

Note: As we're currently in a Grand Siesta, the code is pointed at SIBR's replay feed for testing.
Make sure to update the URL on line 60 to `https://www.blaseball.com/events/streamData` for live feed.