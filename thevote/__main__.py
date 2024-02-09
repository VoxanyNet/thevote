import os
import pickle

from thevote import bot

DISCORD_TOKEN = os.environ["THEVOTE_DISCORD_TOKEN"]
VOTES_PATH = os.environ["THEVOTE_VOTES_PATH"]

bot = bot.TheVote(VOTES_PATH)

bot.run(DISCORD_TOKEN)