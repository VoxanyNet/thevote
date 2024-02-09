import os
import pickle

import discord

from thevote import commands

class TheVote(discord.Bot):
    def __init__(self, votes_path, description=None, *args, **options):

        intents = discord.Intents.default()

        super().__init__(description, intents=intents, *args, **options)

        self.add_application_command(commands.vote)
        self.add_application_command(commands.run)
        self.add_application_command(commands.tally)
        self.add_application_command(commands.candidates)
        self.add_application_command(commands.votingfor)
        self.add_application_command(commands.unvote)

        # create empty votes file if it doesnt exist yet
        if not os.path.exists(votes_path):
            with open(votes_path, "wb") as handle:
                pickle.dump({}, handle)
            
        with open(votes_path, "rb") as handle:
            self.votes = pickle.load(handle)
    
    def save(self):
        # save vote data to disk
        with open("votes.data", "wb") as handle:
            pickle.dump(self.votes, handle)