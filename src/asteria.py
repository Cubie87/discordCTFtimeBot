#
#
# importing packages...
#
#


# Discord libraries
import discord
from discord.ext import commands
# environmental variables for security :D
from dotenv import load_dotenv
import os # reading .env file

# utility libraries
import re # regex

# custom libraries
from variables import botVars
import ctfTime






#
#
# Global variable definition
#
#



# load token from env file
load_dotenv(".env")

# specify what token to grab
discordToken = os.getenv("DISCORD_TOKEN")



# defines permissions
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

# define bot client
client = commands.Bot(
    command_prefix = botVars.prefix,
    help_command = None, # to disable default help command
    strip_after_prefix = True,
    owner_id = botVars.owner,
    intents = intents
)




# startup message in console.
@client.event
async def on_ready(): # do this on startup
    # announces when the bot is up and running
    print(f"{client.user} is now online and is connected to " + str(len(client.guilds)) + " servers: ")
    # list servers by server name where Asteria exists in on bootup.
    # this is done to prevent unauthorised distribution of the bot into unknown servers.
    async for guild in client.fetch_guilds(limit=250):
        print(" - " + guild.name + " - " + str(guild.id))







#
#
# Run commands
#
#




# any normal text commands. This is run first before any of the @client.commands() commands
@client.event
async def on_message(message):
    # don't respond to self
    if message.author == client.user:
        return
    
    # don't respond to DMs
    if isinstance(message.channel, discord.channel.DMChannel):
        return
    
    # continue processing bot commands
    await client.process_commands(message)




# ping the bot! The most basic command.
@client.command()
async def ping(ctx):
    print(ctx.message.author.name + "#" + ctx.message.author.discriminator + " pinged the bot.")
    await ctx.send(embed = discord.Embed(title = "Pong!", color = 0x0078ff))

# help command
@client.command()
async def help(ctx):
    file = open("help.txt", "r")
    await ctx.send(embed = discord.Embed(title = "Asteria's commands", description = file.read(), color = 0x0078ff))
    file.close()


#
# CTFtime commands
#


# send some brief details about a CTFtime entry
@client.command(aliases=['ctf'])
async def ctftime(ctx, *, code):
    # check for valid ID
    if not ctfTime.isCtfCodeValid(code):
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return
    
    # grab the event details
    title, reply = ctfTime.grabCtfDetails(code)
    # errors if the event ID doesn't correspond with an actual ctftime event
    if not title:
        await ctx.send(embed = discord.Embed(title = "Error!", description = "Please input a valid CTFTime ID.\nEg: `=ctftime 1000`", color = 0x880000))
        return
    await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))

# send some brief details about current CTFtimes
@client.command()
async def ctfnow(ctx):
    # grab from RSS feed
    rssFeed = ctfTime.currentCTFs()
    for entry in rssFeed['entries']:
        title, reply = ctfTime.buildReplyRSS(entry)
        await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))
    await ctx.send(embed = discord.Embed(title = "Done", color = 0xFFFFFF))


# send some brief details about upcoming CTFtimes
@client.command()
async def ctfsoon(ctx):
    # grab from RSS feed
    num = 5 # default number to retrieve
    # if the user specified a number to retrieve
    if ctx.message.content != botVars.prefix + "ctfsoon":
        a = ctx.message.content.index(" ")
        num = int(float(ctx.message.content[a+1:]))
    # retrieve and print
    rssFeed = ctfTime.upcomingCTFs()
    # prevent retrieving too many
    if num > len(rssFeed['entries']):
        num = len(rssFeed['entries'])
    if num > 10:
        num = 10
    for entry in rssFeed['entries'][slice(0,num)]:
        title, reply = ctfTime.buildReplyRSS(entry)
        await ctx.send(embed = discord.Embed(title = title, description = reply, color = 0xFFFFFF))
    await ctx.send(embed = discord.Embed(title = "Done", color = 0xFFFFFF))








#
#
# Everything below is administration commands for the bot, for the owner.
#
#




# list all the guilds that the bot is part of
@client.command(hidden = True) # hide it from help command returns.
@commands.is_owner()
async def list(ctx):
    reply = "This bot is connected to " + str(len(client.guilds)) + " servers: \n"
    # list servers by server name where the bot exists in.
    async for guild in client.fetch_guilds(limit=250):
        #print(guild.name)
        reply = reply + " - " + guild.name + " - " + str(guild.id) + "\n"
    await ctx.send(reply)


# Get the bot to leave this guild
@client.command(hidden = True)
@commands.is_owner()
async def bail(ctx, *, ID):
    guild = client.get_guild(int(ID))
    try: 
        print("Bailing from " + guild.name)
        await guild.leave()
        await ctx.send("Successfully left " + guild.name)
    except:
        print("Guild does not exist! ID: " + guild.name)
        await ctx.send("I'm not part of this guild! Check the ID please.")

        
# shut down the bot
@client.command(hidden = True)
@commands.is_owner()
async def sleep(ctx):
    print("Going to sleep....")
    # disconnect from all voice channels.
    for connections in client.voice_clients:
        await connections.disconnect()
        connections.cleanup()
    # send ack
    await ctx.send(embed = discord.Embed(title = "Going to sleep...", color = 0x222222))
    # change status to offline
    await client.change_presence(status=discord.Status.offline)
    # close off the bot
    await client.close()


client.run(discordToken)
