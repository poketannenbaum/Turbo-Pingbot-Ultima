import discord
from discord.ext import tasks, commands
import asyncio
intents = discord.Intents.default()
import re
intents.typing = True
intents.presences = True
intents.message_content = True
intents.dm_messages = True
intents.dm_reactions = True
intents.guild_messages = True
intents.members = True
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="ඞ", intents=intents)
global extracteduid
global stored_message

@tasks.loop()
async def myloop(arg): # Ping Loop
	global stored_message
	if stored_message.author.id != 1: # No idea why I need this tbh.
		while True:
			asyncio.sleep(5)
			await stored_message.channel.send(f"<@{arg}>") # Pinging the poor soul

@bot.event
async def on_ready():
	guild_count = 0 # Generic guild counter
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
@bot.event
async def on_message(message):
	global extracteduid
	global stored_message
	stored_message = message #Setting message data to be globally accessible
	await bot.process_commands(message) #Executing commands
	print(f"Global message is currently: {stored_message.content}") 
	if stored_message.author.id == extracteduid:
		myloop.cancel()
@bot.command(name='turboping') #Command listener
async def turboping(ctx, arg):
	global extracteduid
	global stored_message
	print(f"Received message: {ctx.message.content}")
	print(f"Received argument: {arg}")
	print(f"Received author: {ctx.author.id}")
	user_id_match = re.match(r'<@(\d+)>', arg)
	extracteduid = int(user_id_match.group(1)) #Store extracted 
	print(f"Extracted UID: {extracteduid}") #Extract UID from message
	user = ctx.guild.get_member(extracteduid) #Check if user exists
	if user:
		if extracteduid == "INSERT_BLACKLISTED_ID_HERE": #Test if the UID is on the blacklist
				await stored_message.channel.send(f"No")
		else:
			myloop.start(extracteduid) #Loop procer
	else:
		await stored_message.channel.send(f"User with ID {extracteduid} not found") #Exception for if somone trynna act up

#Token
bot.run("INSERT_BOT_TOKEN_HERE")
