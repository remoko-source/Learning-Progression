import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_API_KEY")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx, chat):
	await ctx.send(f"kamu minta {chat}")

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)
		
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f"Argumen Kurang. (HINT: !ping (sesuatu))")

@bot.event
async def on_ready():
	print(f"BERHASIL AKTIFKAN BOT SEBAGAI {bot.user}")

print("1 + 1 = ?")
tambah = input("> ")
if tambah == "2":
	bot.run(token)
else:
	print("COBA LAGI")