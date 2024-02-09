import discord

@discord.commands.application_command(description="Allow people to vote for you")
async def run(
    ctx: discord.ApplicationContext
):
    
    if ctx.author.id in ctx.bot.votes.keys():
        await ctx.respond("You are already running", ephemeral=True)
        return
    # each candidate starts with zero votes
    ctx.bot.votes[ctx.author.id] = []

    await ctx.respond(f"**{ctx.author.mention}** has been added as a candidate!\n\n**Vote** for them using **/vote {ctx.author.mention}**")

    ctx.bot.save()

@discord.commands.application_command(description="See which candidates you can vote for")
async def candidates(
    ctx: discord.ApplicationContext      
):
    
    candidates_embed = discord.Embed(title="Candidates")

    for candidate_id in ctx.bot.votes.keys():
        
        candidate = await ctx.guild.fetch_member(candidate_id)

        candidates_embed.add_field(
            name=candidate.display_name,
            value=candidate.mention,
            inline=False
        )
    
    await ctx.respond(embed=candidates_embed, ephemeral = True)

@discord.commands.application_command(description="Vote for who you want to win")
async def vote(
    ctx: discord.ApplicationContext,
    candidate: discord.Member
):
    
    # check to see if the candidate voted for is actually a candidate
    if candidate.id not in list(ctx.bot.votes.keys()):
        await ctx.respond("You must vote for a running candidate", ephemeral=True)

        return

    # check if this user already voted for this candidate
    if ctx.author.id in ctx.bot.votes[candidate.id]:
        await ctx.respond("You cannot vote for the same candidate twice", ephemeral=True)
        
        return 
    
    if candidate.id == ctx.author.id:
        await ctx.respond("You cannot vote for yourself", ephemeral = True)

        return

    # add the voter to the list of voters for this candidate
    ctx.bot.votes[candidate.id].append(ctx.author.id)

    await ctx.respond("Your vote has been submitted! ✅", ephemeral=True)

    ctx.bot.save()

@discord.commands.application_command(description="Check who you are voting for")
async def votingfor(
    ctx: discord.ApplicationContext
):
    
    voted_for = []

    voted_for_embed = discord.Embed(title="Voted For")

    for candidate_id, votes in ctx.bot.votes.items():
        if ctx.author.id in votes:
            voted_for.append(candidate_id)
    
    for candidate_id in voted_for:
        
        candidate = await ctx.guild.fetch_member(candidate_id)

        voted_for_embed.add_field(
            name=candidate.display_name,
            value=candidate.mention,
            inline=False
        )
    
    await ctx.respond("This is who you have voted for: ", embed = voted_for_embed, ephemeral = True)
    
@discord.commands.application_command(description="Remove your vote for a candidate")
async def unvote(
    ctx: discord.ApplicationContext,
    candidate: discord.Member
):
    
    # check to see if the candidate voted for is actually a candidate
    if candidate.id not in list(ctx.bot.votes.keys()):
        await ctx.respond("You cannot unvote someone who is not a candidate", ephemeral=True)

        return

    # check if this user already voted for this candidate
    if ctx.author.id not in ctx.bot.votes[candidate.id]:
        await ctx.respond("You haven't voted for this person", ephemeral=True)
        
        return 
    
    ctx.bot.votes[candidate.id].remove(ctx.author.id)

    await ctx.respond(f"Your vote for {candidate.mention} has been removed", ephemeral=True)

@discord.commands.application_command(description="Tally the results")
async def tally(
    ctx: discord.ApplicationContext
):

    # sort the votes
    sorted_votes = dict(sorted(ctx.bot.votes.items(), key=lambda item: len(item[1]), reverse=True))

    #print(sorted_votes)
    
    winner = await ctx.guild.fetch_member(list(sorted_votes.keys())[0])

    # check for ties jankily
    ties = []
    for candidate_id, votes in sorted_votes.items():

        if votes == sorted_votes[winner.id]:
            ties.append(candidate_id)

    # create an embed to display the votes for each candidate
    tally_embed = discord.Embed(title="Vote Tally")

    for candidate_id, votes in sorted_votes.items():
        
        candidate = await ctx.guild.fetch_member(candidate_id)

        tally_embed.add_field(
            name=f"**{len(votes)}** votes",
            value=candidate.mention,
            inline=False
        )

    # technically the winner always ties with themselves
    if len(ties) == 1:
        await ctx.respond(f"The winner of the vote is: {winner.mention}", embed=tally_embed)

    else:

        # this is jank
        tied_candidate_mentions = []

        for candidate_id in ties:
            candidate = await ctx.guild.fetch_member(candidate_id)

            tied_candidate_mentions.append(candidate.mention)

        await ctx.respond(f"The vote is **tied** between {' and '.join(tied_candidate_mentions)}")