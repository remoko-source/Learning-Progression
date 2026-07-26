#Mini Project day 04
#Live Price Bot
from dotenv import load_dotenv
from tabulate import tabulate
from discord.ext import commands
import os
import discord
import aiohttp
#=================================================
load_dotenv()
WEBHOOK = os.getenv("WEBHOOK_API_URL")
URL = os.getenv("URL_COIN_API")
BOT_KEY = os.getenv("BOT_API_KEY")
#=================================================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch(url, params):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params) as response:
			response.raise_for_status()
			return await response.json()

class SalahFormat2(Exception):
	pass
class SalahFormat1(Exception):
	pass

async def table_maker(ctx,coins,data):
	hasil = []
	for i, coin in enumerate(coins, start=1):
		if coin not in data:
			hasil.append({"No" : i,"Coins": coin.title(), "Harga": "INVALID"})
		else:
			hasil.append({
			"No" : i,
			"Coins" : coin.title(),
			"Harga" : f'{data[coin]["usd"]}'
			})
	contents = tabulate(hasil, headers="keys",tablefmt="grid",colalign=("left","center","right"))
	async with aiohttp.ClientSession() as session:
		async with session.post(WEBHOOK, json={"content" : f"```\n{contents}\n```"}) as response:
			response.raise_for_status()
		

@bot.command()
async def prices(ctx, *coin_names):
	if len(coin_names) <= 1:
		raise SalahFormat2()
	params = {
	"ids" : ",".join(coin_names),
	"vs_currencies" : "usd"
	}
	hasil = await fetch(URL,params)
	await table_maker(ctx,coin_names,hasil)
	

@bot.command()
async def price(ctx, coin_name):
	if not coin_name:
		raise SalahFormat1()
	params = {
	"ids" : coin_name,
	"vs_currencies" : "usd"
	}
	hasil = await fetch(URL,params)
	await table_maker(ctx,[coin_name],hasil)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandInvokeError):
		if isinstance(error.original, SalahFormat1):
			await ctx.send("HARAP MASUKKAN DENGAN FORMAT : !price (coin)")
		elif isinstance(error.original, SalahFormat2):
			await ctx.send("HARAP MASUKKAN DENGAN FORMAT : !prices (coin1 coin2 dst)")
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print("BOT DIJALANKAN")

bot.run(BOT_KEY)